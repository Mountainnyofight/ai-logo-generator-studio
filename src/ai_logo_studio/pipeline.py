"""Generation pipeline. Ordered stages, plugin hooks between them."""
from __future__ import annotations

import time
from pathlib import Path

from rich.console import Console

from logo_kernels.diffusion import DiffusionKernel
from logo_kernels.vectorizer import Vectorizer
from shared_contracts.artifact import GenerationResult, LogoArtifact
from .config import StudioConfig
from .registry import PluginRegistry

console = Console()

class GenerationPipeline:
    def __init__(self, config: StudioConfig, registry: PluginRegistry) -> None:
        self.config = config
        self.registry = registry
        self.diffusion = DiffusionKernel(config.device)
        self.vectorizer = Vectorizer(backend=config.stages.get("vectorize", {}).get("backend", "auto"))

    async def run(self, prompt: str, out_dir: Path, name: str) -> GenerationResult:
        out_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.perf_counter()

        cleaned = self._run_hooks("pre_prompt", prompt)
        raster = self.diffusion.sample(
            prompt=cleaned,
            steps=self.config.stages.get("diffuse", {}).get("steps", 28),
            size=tuple(self.config.stages.get("diffuse", {}).get("size", (1024, 1024))),
        )
        raster = self._run_hooks("post_diffuse", raster)
        vector = self.vectorizer.trace(raster)
        vector = self._run_hooks("post_vectorize", vector)

        artifact = LogoArtifact(prompt=cleaned, raster=raster, vector=vector)
        result = self._export(artifact, out_dir)
        console.log(f"[dim]pipeline {name} done in {time.perf_counter() - t0:.2f}s[/dim]")
        return result

    def _run_hooks(self, capability: str, payload):
        for plugin in self.registry.for_capability(capability):
            try:
                payload = plugin.apply(payload)
            except Exception as exc:  # noqa: BLE001
                console.log(f"[red]plugin {plugin.manifest.name} failed: {exc}[/red]")
        return payload

    def _export(self, artifact: LogoArtifact, out_dir: Path) -> GenerationResult:
        svg_path = out_dir / "logo.svg"
        png_path = out_dir / "logo.png"
        svg_path.write_text(artifact.vector.to_svg(), encoding="utf-8")
        artifact.raster.save(png_path)
        return GenerationResult(primary=svg_path, sidecars=[png_path])