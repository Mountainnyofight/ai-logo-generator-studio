"""Host bootstrap: wires config, registry, loader, and pipeline together."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from shared_contracts.artifact import GenerationResult
from .config import StudioConfig
from .loader import PluginLoader
from .pipeline import GenerationPipeline
from .registry import PluginRegistry

console = Console()

@dataclass
class StudioHost:
    config: StudioConfig
    registry: PluginRegistry
    loader: PluginLoader
    pipeline: GenerationPipeline

    @classmethod
    def from_config(cls, path: Path | None = None) -> "StudioHost":
        cfg = StudioConfig.load(path)
        registry = PluginRegistry()
        loader = PluginLoader(cfg, registry)
        loader.discover_entrypoints()
        loader.discover_paths()
        pipeline = GenerationPipeline(cfg, registry)
        console.log(f"[dim]host up — {len(registry.manifests())} plugins[/dim]")
        return cls(cfg, registry, loader, pipeline)

    def reload_plugins(self) -> None:
        self.registry.clear()
        self.loader.discover_entrypoints()
        self.loader.discover_paths()

    async def generate(self, prompt: str, out_dir: Path, pipeline: str) -> GenerationResult:
        return await self.pipeline.run(prompt=prompt, out_dir=out_dir, name=pipeline)