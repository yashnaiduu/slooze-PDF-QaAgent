import logging
from pathlib import Path

from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str | Path) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append(text)
        else:
            logger.warning(f"No extractable text on page {i + 1}")

    if not pages:
        raise ValueError(f"No text content extracted from {path.name}")

    full_text = "\n\n".join(pages)
    logger.info(f"Extracted {len(full_text)} chars from {len(reader.pages)} pages ({path.name})")
    return full_text


def extract_text_from_bytes(data: bytes, filename: str = "upload.pdf") -> str:
    import io

    reader = PdfReader(io.BytesIO(data))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append(text)

    if not pages:
        raise ValueError(f"No text content extracted from {filename}")

    full_text = "\n\n".join(pages)
    logger.info(f"Extracted {len(full_text)} chars from {len(reader.pages)} pages ({filename})")
    return full_text
