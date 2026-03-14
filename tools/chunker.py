import logging
from dataclasses import dataclass
from typing import List

from config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class TextChunk:
    text: str
    index: int
    metadata: dict


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    source: str = "",
) -> List[TextChunk]:
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: List[TextChunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = start + chunk_size

        # try to break at sentence boundary
        if end < len(text):
            boundary = text.rfind(". ", start, end)
            if boundary > start:
                end = boundary + 1

        chunk_text_str = text[start:end].strip()
        if chunk_text_str:
            chunks.append(
                TextChunk(
                    text=chunk_text_str,
                    index=index,
                    metadata={"source": source, "start_char": start, "end_char": end},
                )
            )
            index += 1

        start = end - chunk_overlap if end < len(text) else len(text)

    logger.info(f"Split text into {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    return chunks
