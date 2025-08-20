from typing import Optional


def build_caption_prompt(
    *,
    language: str,
    tone: str,
    context: Optional[str] = None,
    min_captions: int = 4,
    max_captions: int = 5,
    format_style: str = "plain",  # "plain" | "numbered"
) -> str:
    parts: list[str] = []
    parts.append(
      (
        f"Generate {min_captions}-{max_captions} descriptive and diverse captions for the provided image "
        f"in {language} with a {tone} tone. Each caption should reflect a different perspective or focus."
      )
    )

    if context:
      parts.append(
        f"Incorporate the following context if relevant: {context}")

    if format_style == "numbered":
      parts.append(
        "Return only a numbered list starting at 1, one caption per line, with no extra commentary."
      )
      parts.append("Example:\n1. Caption 1\n2. Caption 2\n3. Caption 3")
    else:
      parts.append(
        "Return only the captions, one per line, with no numbering, bullets, quotes, or extra text."
      )

    return " ".join(parts)


def build_hashtag_prompt(*, language: str, tone: str, context: Optional[str] = None, count: int = 10) -> str:
    parts: list[str] = []
    parts.append(
        f"Generate {count} relevant social media hashtags in {language} with a {tone} tone for the provided image."
    )
    if context:
        parts.append(f"Consider this context: {context}")
    parts.append("Return only hashtags separated by spaces, no extra text.")
    return " ".join(parts)


def build_elements_prompt(*, language: str) -> str:
    return (
        f"List distinct visual elements you can see in the image in {language}. "
        "Return only a single comma-separated list, no extra text."
    )
