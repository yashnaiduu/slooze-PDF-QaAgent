import logging
from typing import List

import numpy as np

from config.settings import settings

logger = logging.getLogger(__name__)

_model_cache = {}


class EmbeddingService:
    def __init__(self, model_name: str | None = None):
        self._model_name = model_name or settings.EMBEDDING_MODEL
        self._model = self._load_model()

    def _load_model(self):
        if self._model_name in _model_cache:
            return _model_cache[self._model_name]

        from sentence_transformers import SentenceTransformer

        logger.info(f"Loading embedding model: {self._model_name}")
        model = SentenceTransformer(self._model_name)
        _model_cache[self._model_name] = model
        return model

    def embed(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.array([])
        embeddings = self._model.encode(texts, show_progress_bar=False)
        return np.array(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        return self.embed([query])[0]

    @property
    def dimension(self) -> int:
        return self._model.get_sentence_embedding_dimension()
