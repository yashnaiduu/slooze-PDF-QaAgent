import logging
from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np

from config.settings import settings

logger = logging.getLogger(__name__)


class VectorStore(ABC):
    @abstractmethod
    def add(self, embeddings: np.ndarray, texts: List[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError


class FAISSVectorStore(VectorStore):
    def __init__(self, dimension: int):
        import faiss

        self._index = faiss.IndexFlatIP(dimension)
        self._texts: List[str] = []

    def add(self, embeddings: np.ndarray, texts: List[str]) -> None:
        import faiss

        # L2-normalize for cosine similarity with inner product index
        faiss.normalize_L2(embeddings)
        self._index.add(embeddings)
        self._texts.extend(texts)
        logger.info(f"Added {len(texts)} vectors (total: {self._index.ntotal})")

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        import faiss

        query = query_embedding.reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(query)
        scores, indices = self._index.search(query, min(top_k, self._index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx < len(self._texts):
                results.append((self._texts[idx], float(score)))
        return results

    def clear(self) -> None:
        self._index.reset()
        self._texts.clear()

    def size(self) -> int:
        return self._index.ntotal


class ChromaVectorStore(VectorStore):
    def __init__(self, collection_name: str = "documents"):
        import chromadb

        self._client = chromadb.Client()
        self._collection = self._client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )
        self._counter = 0

    def add(self, embeddings: np.ndarray, texts: List[str]) -> None:
        ids = [f"doc_{self._counter + i}" for i in range(len(texts))]
        self._collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            ids=ids,
        )
        self._counter += len(texts)
        logger.info(f"Added {len(texts)} vectors to Chroma (total: {self._counter})")

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        result = self._collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(top_k, self._collection.count()),
        )
        texts = result["documents"][0] if result["documents"] else []
        distances = result["distances"][0] if result["distances"] else []

        return [(text, 1 - dist) for text, dist in zip(texts, distances)]

    def clear(self) -> None:
        import chromadb

        client = chromadb.Client()
        try:
            client.delete_collection("documents")
        except Exception:
            pass
        self._collection = client.get_or_create_collection(
            name="documents", metadata={"hnsw:space": "cosine"}
        )
        self._counter = 0

    def size(self) -> int:
        return self._collection.count()


def get_vector_store(dimension: int) -> VectorStore:
    store_type = settings.VECTOR_STORE_TYPE.lower()
    if store_type == "faiss":
        return FAISSVectorStore(dimension)
    elif store_type == "chroma":
        return ChromaVectorStore()
    else:
        raise ValueError(f"Unsupported vector store: {store_type}. Supported: faiss, chroma")
