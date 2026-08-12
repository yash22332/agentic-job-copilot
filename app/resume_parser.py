"""
Resume Parser

Responsible for extracting plain text from resume files.
"""

from pathlib import Path

import pdfplumber


def parse_resume(file_path: str) -> str:
    """
    Read a resume file and return its text.

    Currently supports TXT and PDF files.

    Args:
        file_path: Path to the resume file.

    Returns:
        Extracted resume text.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is unsupported.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume not found: {file_path}"
        )

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".pdf":
        return _parse_pdf(path)

    raise ValueError(
        f"Unsupported resume format: {path.suffix}"
    )


def _parse_pdf(path: Path) -> str:
    """Extract text from a PDF resume."""

    pages_text: list[str] = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                pages_text.append(text)

    return "\n".join(pages_text).strip()