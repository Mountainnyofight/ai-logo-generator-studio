"""SVG export plugin. Adds a minified SVG sidecar and strips editor metadata."""
from __future__ import annotations

import re

from shared_contracts.plugin import LogoPlugin, PluginManifest

PLUGIN_MANIFEST = PluginManifest(
    name="svg_export", version="0.3.1",
    capabilities=["post_vectorize"], author="studio", api=1,
)

_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)

class SVGExportPlugin(LogoPlugin):
    manifest = PLUGIN_MANIFEST

    def apply(self, payload):
        if not hasattr(payload, "to_svg"):
            return payload
        svg = _COMMENT.sub("", payload.to_svg())
        svg =