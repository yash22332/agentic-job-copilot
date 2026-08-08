"""
Prompt Loader

Loads prompt templates from the prompts directory.
"""

from pathlib import Path


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """
    Load a prompt template from the prompts directory.

    Args:
        filename: Name of the prompt file.

    Returns:
        Prompt text as a string.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """

    prompt_path = PROMPTS_DIR / filename

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {filename}"
        )

    return prompt_path.read_text(encoding="utf-8")