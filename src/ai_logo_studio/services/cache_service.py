"""Disk cache for generated artifacts, keyed by prompt+params digest."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

class ArtifactCache:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def key(self, prompt: str, params: dict) -> str:
        payload = json.dumps({"p": prompt, "k": params}, sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()[:16]

    def path_for(self, key: str) -> Path:
        return self.root / key

    def has(self, key: str) -> bool:
        return self.path_for(key).exists()