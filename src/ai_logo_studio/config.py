"""Config loading. TOML on disk -> typed StudioConfig."""
from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

class StudioConfig(BaseModel):
    pipeline_name: str = "default"
    plugin_paths: list[Path] = Field(default_factory=lambda: [Path("src/plugins")])
    out_dir: Path = Path("out")
    watch_plugins: bool = False
    device: str = "cuda"
    cache_dir: Path = Path(".cache/logo_studio")
    stages: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def load(cls, path: Path | None = None) -> "StudioConfig":
        root = Path(__file__).resolve().parents[2]
        cfg_path = path or (root / "config" / "default_pipeline.toml")
        data: dict[str, Any] = {}
        if cfg_path.exists():
            with cfg_path.open("rb") as fh:
                data = tomllib.load(fh)
        stages = {k.split(".", 1)[1]: v for k, v in data.items() if k.startswith("stage.")}
        meta = data.get("meta", {})
        return cls(
            pipeline_name=meta.get("name", "default"),
            stages=stages,
            out_dir=root / "out",
        )