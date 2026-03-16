import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from config.settings import settings
from services.embedding_service import EmbeddingService
from services.llm_provider import LLMProvider, get_provider
from services.retrieval_service import RetrievalService
from tools.chunker import chunk_text
from tools.pdf_loader import extract_text_from_pdf, extract_text_from_bytes
from vectorstore.vector_store import get_vector_store

logger = logging.getLogger(__name__)

QA_SYSTEM_PROMPT = (
    "You are an AI Document Assistant. Answer the user's question using ONLY "
    "the provided document context. Be precise and concise. "
    "Never reference internal details like chunk numbers, relevance scores, "
    "or how the document was processed. If the context is insufficient, state that clearly."
)

SUMMARY_SYSTEM_PROMPT = (
    "You are an AI Document Summarizer. Provide a comprehensive yet concise "
    "summary of the document based on the provided text excerpts. Organize "
    "the summary logically with key points and main themes."
)


@dataclass
class RAGResponse:
    answer: str
    sources: List[str] = field(default_factory=list)
    num_chunks_used: int = 0


class RAGAgent:
    def __init__(self, llm: LLMProvider | None = None):
        self._llm = llm or get_provider()
        self._embedding_service = EmbeddingService()
        self._store = get_vector_store(self._embedding_service.dimension)
        self._retrieval = RetrievalService(self._embedding_service, self._store)
        self._document_text: str = ""

    def ingest_file(self, file_path: str | Path) -> int:
        self._retrieval.clear()
        self._document_text = extract_text_from_pdf(file_path)
        chunks = chunk_text(self._document_text, source=str(file_path))
        count = self._retrieval.index_chunks([c.text for c in chunks])
        logger.info(f"Ingested {count} chunks from {file_path}")
        return count

    def ingest_bytes(self, data: bytes, filename: str = "upload.pdf") -> int:
        self._retrieval.clear()
        self._document_text = extract_text_from_bytes(data, filename)
        chunks = chunk_text(self._document_text, source=filename)
        count = self._retrieval.index_chunks([c.text for c in chunks])
        logger.info(f"Ingested {count} chunks from {filename}")
        return count

    def query(self, question: str) -> RAGResponse:
        if self._retrieval.index_size == 0:
            return RAGResponse(answer="No document has been ingested yet. Please upload a PDF first.")

        results = self._retrieval.retrieve(question)
        if not results:
            return RAGResponse(answer="No relevant context found for your question.")

        context = self._build_context(results)
        prompt = f"User Question: {question}\n\nDocument Context:\n{context}"

        try:
            answer = self._llm.generate(prompt, system_prompt=QA_SYSTEM_PROMPT)
        except Exception as exc:
            logger.error(f"LLM generation failed: {exc}")
            return RAGResponse(answer=f"Error generating answer: {exc}")

        return RAGResponse(
            answer=answer,
            sources=[f"Section (score: {score:.3f})" for _, score in results],
            num_chunks_used=len(results),
        )

    def summarize(self) -> RAGResponse:
        if not self._document_text:
            return RAGResponse(answer="No document has been ingested yet.")

        # use beginning + sampled chunks for a representative summary
        max_context = settings.LLM_MAX_TOKENS * 3
        text_for_summary = self._document_text[:max_context]

        prompt = f"Document Text:\n{text_for_summary}"

        try:
            answer = self._llm.generate(prompt, system_prompt=SUMMARY_SYSTEM_PROMPT)
        except Exception as exc:
            logger.error(f"LLM summarization failed: {exc}")
            return RAGResponse(answer=f"Error generating summary: {exc}")

        return RAGResponse(answer=answer)

    @staticmethod
    def _build_context(results: list) -> str:
        parts = []
        for i, (text, score) in enumerate(results, 1):
            parts.append(f"[Section {i}]\n{text}\n---")
        return "\n".join(parts)
