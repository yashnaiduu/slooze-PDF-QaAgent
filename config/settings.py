from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 2048

    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    ANTHROPIC_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_PROVIDER: str = "sentence_transformers"

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    VECTOR_STORE_TYPE: str = "faiss"
    TOP_K: int = 5

    LOG_LEVEL: str = "INFO"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000


settings = Settings()
