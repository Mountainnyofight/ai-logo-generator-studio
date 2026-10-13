"""Prompt cleaning + trademark scrubbing before diffusion."""
from __future__ import annotations

import re

TRADEMARK_HINTS = re.compile(
    r"\b(?:nike|adidas|apple|google|microsoft|disney|marvel|nintendo|sony)\b",
    re.IGNORECASE,
)

def clean(prompt: str, *, strip_trademarks: bool = True, max_tokens: int = 77) -> str:
    text = " ".join(prompt.strip().split())
    if strip_trademarks:
        text = TRADEMARK_HINTS.sub("", text)
    words = text.split()
    if len(words) > max_tokens:
        words = words[:max_tokens]
    return " ".join(words).strip() or "minimal geometric logo mark"