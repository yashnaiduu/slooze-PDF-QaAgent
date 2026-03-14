import logging
from abc import ABC, abstractmethod

from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    def __init__(self):
        from openai import OpenAI

        kwargs = {"api_key": settings.OPENAI_API_KEY}
        if settings.OPENAI_BASE_URL:
            kwargs["base_url"] = settings.OPENAI_BASE_URL
        self._client = OpenAI(**kwargs)

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), reraise=True)
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    def __init__(self):
        from anthropic import Anthropic

        self._client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), reraise=True)
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        kwargs = {
            "model": settings.LLM_MODEL,
            "max_tokens": settings.LLM_MAX_TOKENS,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self._client.messages.create(**kwargs)
        return response.content[0].text


class OllamaProvider(LLMProvider):
    def __init__(self):
        import httpx

        self._base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self._client = httpx.Client(timeout=120)

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), reraise=True)
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        payload = {
            "model": settings.LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": settings.LLM_TEMPERATURE},
        }
        if system_prompt:
            payload["system"] = system_prompt

        response = self._client.post(f"{self._base_url}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()["response"]


_PROVIDERS = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "ollama": OllamaProvider,
    "openai_compatible": OpenAIProvider,
}


def get_provider() -> LLMProvider:
    provider_name = settings.LLM_PROVIDER.lower()
    provider_cls = _PROVIDERS.get(provider_name)
    if provider_cls is None:
        raise ValueError(
            f"Unsupported LLM provider '{provider_name}'. "
            f"Supported: {list(_PROVIDERS.keys())}"
        )
    logger.info(f"Initializing LLM provider: {provider_name}")
    return provider_cls()
