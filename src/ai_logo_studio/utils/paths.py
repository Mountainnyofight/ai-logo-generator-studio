"""Path safety. All cache/out writes confined under a single root."""
from __future__ import annotations

from pathlib import Path

class UnsafePathError(ValueError):
    pass

def confined(root: Path, candidate: Path) -> Path:
    root = root.resolve()
    target = (root / candidate).resolve()
    if root not in target.parents and target != root:
        raise UnsafePathError(f"path escapes root: {candidate}")
    return target