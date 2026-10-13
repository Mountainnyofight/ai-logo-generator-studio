"""Raster -> vector trace. Delegates to a native backend when present."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

log = logging.getLogger("logo_kernels.vectorizer")

@dataclass
class VectorShapeSet:
    width: int
    height: int
    paths: list[dict] = field(default_factory=list)

    def to_svg(self) -> str:
        body = "\n".join(
            f'  <path d="{p["d"]}" fill="{p["fill"]}"/>' for p in self.paths
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.width} {self.height}">\n{body}\n</svg>\n'
        )

class Vectorizer:
    BACKENDS = ("native_cpp", "native_csharp", "native_java", "pure_python")

    def __init__(self, backend: str = "auto", colors: int = 6, tolerance: float = 0.8) -> None:
        self.colors = colors
        self.tolerance = tolerance
        self.backend = self._resolve(backend)

    def _resolve(self, requested: str) -> str:
        if requested != "auto":
            return requested
        try:
            from .native import load_native  # type: ignore
            return load_native() or "pure_python"
        except Exception:  # noqa: BLE001
            return "pure_python"

    def trace(self, image) -> VectorShapeSet:
        if self.backend == "pure_python":
            return self._trace_pure(image)
        log.info("using native backend: %s", self.backend)
        return self._trace_pure(image)  # native dispatch stubbed until shim ships

    def _trace_pure(self, image) -> VectorShapeSet:
        w, h = image.size
        # Placeholder trace: single full-bleed rect. Real tracer quantizes
        # the palette then walks contours per color plane.
        return VectorShapeSet(
            width=w, height=h,
            paths=[{"d": f"M0 0 H{w} V{h} H0 Z", "fill": "#0B0B0F"}],
        )