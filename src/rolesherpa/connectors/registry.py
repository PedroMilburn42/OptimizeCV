"""Loads the connector registry from config/sources.yaml (design.md D4).
Re-read fresh on every construction rather than cached at process scope.
"""

import importlib
from dataclasses import dataclass
from pathlib import Path

import yaml

from rolesherpa.domain.ports import JobSourcePort

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "sources.yaml"


@dataclass
class BlockedSource:
    name: str
    blocked_reason: str


def _load_class(module_path: str) -> type:
    module_name, _, class_name = module_path.partition(":")
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class ConnectorRegistry:
    def __init__(self, config_path: Path | None = None):
        path = config_path or DEFAULT_CONFIG_PATH
        data = yaml.safe_load(path.read_text())
        self._sources: dict = data.get("sources", {})

    def active_connectors(self) -> dict[str, JobSourcePort]:
        connectors = {}
        for name, entry in self._sources.items():
            if entry.get("enabled") and entry.get("module"):
                connector_class = _load_class(entry["module"])
                connectors[name] = connector_class()
        return connectors

    def blocked_sources(self) -> list[BlockedSource]:
        return [
            BlockedSource(name=name, blocked_reason=entry["blocked_reason"])
            for name, entry in self._sources.items()
            if "blocked_reason" in entry
        ]
