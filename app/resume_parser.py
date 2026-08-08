"""
Resume Parser

Responsible for reading resume files.
"""

from pathlib import Path


def parse_resume(file_path: str) -> str:
    """
    Read a text resume and return its contents.

    Args:
        file_path: Path to the resume file.

    Returns:
        Resume text.

    Raises:
        FileNotFoundError:
            If the file does not exist.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume not found: {file_path}"
        )

    return path.read_text(encoding="utf-8")