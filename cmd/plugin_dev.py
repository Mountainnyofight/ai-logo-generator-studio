"""Scaffold a new plugin package under src/plugins/."""
from __future__ import annotations

import re
import sys
from pathlib import Path

TEMPLATE = '''"""Auto-scaffolded plugin: {name}."""
from __future__ import annotations

from shared_contracts.plugin import LogoPlugin, PluginManifest

PLUGIN_MANIFEST = PluginManifest(
    name="{name}",
    version="0.1.0",
    capabilities=["{capability}"],
    author="you",
)


class {cls}(LogoPlugin):
    manifest = PLUGIN_MANIFEST

    def apply(self, ctx):
        # ctx.logo : LogoArtifact, ctx.config : dict
        return ctx.logo
'''

def _slug(raw: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", raw.lower())

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: plugin_dev.py <plugin_name> [capability]")
        return 2
    name = _slug(sys.argv[1])
    capability = sys.argv[2] if len(sys.argv) > 2 else "postprocess"
    cls = "".join(p.title() for p in name.split("_")) + "Plugin"
    root = Path(__file__).resolve().parents[1] / "src" / "plugins" / name
    root.mkdir(parents=True, exist_ok=True)
    (root / "__init__.py").write_text("")
    (root / "plugin.py").write_text(TEMPLATE.format(name=name, cls=cls, capability=capability))
    print(f"scaffolded -> {root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())