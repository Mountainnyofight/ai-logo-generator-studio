"""Contracts shared between host and plugins. Frozen surface — bump major to change."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol

from pydantic import BaseModel, Field

class PluginManifest(BaseModel):
    name: str
    version: str
    capabilities: list[str] = Field(default_factory=list)
    author: str = "unknown"
    requires: list[str] = Field(default_factory=list)
    api: int = 1

class PluginContext(BaseModel):
    prompt: str
    config: dict[str, Any] = Field(default_factory=dict)
    model_config = {"arbitrary_types_allowed": True}

class LogoPlugin(ABC):
    manifest: PluginManifest

    @abstractmethod
    def apply(self, payload: Any) -> Any:
        """Transform `payload` and return it. Must not mutate in place."""

class CapabilityHook(Protocol):
    capability: str
    def __call__(self, payload: Any) -> Any: ...