import logging
from typing import List, Tuple

from config.settings import settings
from services.embedding_service import EmbeddingService
from vectorstore.vector_store import VectorStore

logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(self, embedding_service: EmbeddingService, store: VectorStore):
        self._embeddings = embedding_service
        self._store = store

    def index_chunks(self, texts: List[str]) -> int:
        if not texts:
            return 0
        embeddings = self._embeddings.embed(texts)
        self._store.add(embeddings, texts)
        return len(texts)

    def retrieve(self, query: str, top_k: int | None = None) -> List[Tuple[str, float]]:
        top_k = top_k or settings.TOP_K
        query_vec = self._embeddings.embed_query(query)
        results = self._store.search(query_vec, top_k=top_k)
        logger.info(f"Retrieved {len(results)} chunks for query: '{query[:60]}...'")
        return results

    def clear(self) -> None:
        self._store.clear()

    @property
    def index_size(self) -> int:
        return self._store.size()
