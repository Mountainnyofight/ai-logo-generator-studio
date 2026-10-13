"""In-memory plugin registry. Capability-indexed for fast lookup in the pipeline."""
from __future__ import annotations

from collections import defaultdict

from shared_contracts.plugin import LogoPlugin, PluginManifest

class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, LogoPlugin] = {}
        self._manifests: dict[str, PluginManifest] = {}
        self._by_capability: dict[str, list[str]] = defaultdict(list)
        self._sources: dict[str, str] = {}

    def register(self, plugin: LogoPlugin, manifest: PluginManifest, source: str) -> None:
        if manifest.name in self._plugins:
            raise ValueError(f"duplicate plugin name: {manifest.name}")
        self._plugins[manifest.name] = plugin
        self._manifests[manifest.name] = manifest
        self._sources[manifest.name] = source
        for cap in manifest.capabilities:
            self._by_capability[cap].append(manifest.name)

    def clear(self) -> None:
        self._plugins.clear()
        self._manifests.clear()
        self._by_capability.clear()
        self._sources.clear()

    def get(self, name: str) -> LogoPlugin:
        return self._plugins[name]

    def for_capability(self, capability: str) -> list[LogoPlugin]:
        return [self._plugins[n] for n in self._by_capability.get(capability, [])]

    def manifests(self) -> list[PluginManifest]:
        return list(self._manifests.values())

    def source_of(self, name: str) -> str:
        return self._sources.get(name, "<unknown>")