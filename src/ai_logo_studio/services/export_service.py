"""Export helpers: SVG -> PNG/PDF via cairosvg, with graceful fallback."""
from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger("ai_logo_studio.export")

def svg_to_png(svg_text: str, dest: Path, size: int = 1024) -> bool:
    try:
        import cairosvg  # type: ignore
    except ImportError:
        log.warning("cairosvg not installed — skipping PNG sidecar export")
        return False
    cairosvg.svg2png(bytestring=svg_text.encode(), write_to=str(dest),
                     output_width=size, output_height=size)
    return True

def svg_to_pdf(svg_text: str, dest: Path) -> bool:
    try:
        import cairosvg  # type: ignore
    except ImportError:
        log.warning("cairosvg not installed — skipping PDF export")
        return False
    cairosvg.svg2pdf(bytestring=svg_text.encode(), write_to=str(dest))
    return True