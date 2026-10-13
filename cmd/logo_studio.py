"""CLI bootstrap. Thin shim so `python cmd/logo_studio.py` works without install."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ai_logo_studio.__main__ import app  # noqa: E402

if __name__ == "__main__":
    app()