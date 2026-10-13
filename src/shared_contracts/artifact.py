"""Artifact contracts returned by the pipeline."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict

class LogoArtifact(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    prompt: str
    raster: object      # PIL.Image.Image
    vector: object      # logo_kernels.vectorizer.VectorShapeSet

class GenerationResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    primary: Path
    sidecars: list[Path] = []