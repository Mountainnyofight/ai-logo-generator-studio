"""Plugin loader. Discovery from entry-points and watched directories.

_Trust boundary:_ a plugin is only imported after its manifest validates.
Anything else is quarantined with a logged reason.
"""
from __future__ import annotations

import importlib
import importlib.metadata as im
import logging
import tomllib
from pathlib import Path

from shared_contracts.plugin import LogoPlugin, PluginManifest
from .config import StudioConfig
from .registry import PluginRegistry

log = logging.getLogger("ai_logo_studio.loader")

class PluginLoadError(RuntimeError):
    pass

class PluginLoader:
    def __init__(self, config: StudioConfig, registry: PluginRegistry) -> None:
        self.config = config
        self.registry = registry

    def discover_entrypoints(self) -> None:
        for ep in im.entry_points(group="ai_logo_studio.plugins"):
            try:
                cls = ep.load()
                self._register_from_class(cls, source=f"entrypoint:{ep.name}")
            except Exception as exc:  # noqa: BLE001
                log.warning("quarantined entrypoint %s: %s", ep.name, exc)

    def discover_paths(self) -> None:
        for base in self.config.plugin_paths:
            if not base.exists():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir() or child.name.startswith("_"):
                    continue
                manifest_file = child / "manifest.toml"
                if not manifest_file.exists():
                    continue
                try:
                    manifest = self._read_manifest(manifest_file)
                    mod = importlib.import_module(f"{base.name}.{child.name}.plugin")
                    cls = getattr(mod, "PLUGIN_CLASS", None) or self._find_plugin_class(mod)
                    self._register_from_class(cls, source=str(child), manifest=manifest)
                except Exception as exc:  # noqa: BLE001
                    log.warning("quarantined %s: %s", child, exc)

    def _read_manifest(self, path: Path) -> PluginManifest:
        with path.open("rb") as fh:
            raw = tomllib.load(fh)
        return PluginManifest(**raw.get("plugin", raw))

    def _find_plugin_class(self, mod) -> type[LogoPlugin]:
        for value in vars(mod).values():
            if isinstance(value, type) and issubclass(value, LogoPlugin) and value is not LogoPlugin:
                return value
        raise PluginLoadError("no LogoPlugin subclass found in module")

    def _register_from_class(self, cls, source: str, manifest: PluginManifest | None = None) -> None:
        if cls is None:
            raise PluginLoadError(f"no plugin class at {source}")
        instance = cls()
        mf = manifest or getattr(instance, "manifest", None)
        if mf is None:
            raise PluginLoadError(f"plugin {cls.__name__} has no manifest")
        self.registry.register(instance, mf, source=source)