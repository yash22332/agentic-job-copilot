"""
Prompt Builder

Builds prompts by replacing placeholders in prompt templates.
"""


def build_prompt(template: str, **kwargs) -> str:
    """
    Replace placeholders in a prompt template.

    Example:
        template = "Hello {{name}}"

        build_prompt(template, name="Yash")

        -> "Hello Yash"
    """

    prompt = template

    for key, value in kwargs.items():
        placeholder = "{{" + key + "}}"

        prompt = prompt.replace(placeholder, value)

    return prompt