from pathlib import Path

import pytest

from rolesherpa.connectors.linkedin import LinkedInConnector
from rolesherpa.connectors.registry import ConnectorRegistry, DEFAULT_CONFIG_PATH

FIXTURE_YAML = """
sources:
  linkedin:
    enabled: true
    module: rolesherpa.connectors.linkedin:LinkedInConnector
  freehire:
    enabled: false
    module: rolesherpa.connectors.freehire:FreehireConnector
  buscojobs:
    enabled: false
    blocked_reason: robots.txt disallows Claude-derived agents.
"""


def _write_config(tmp_path: Path) -> Path:
    path = tmp_path / "sources.yaml"
    path.write_text(FIXTURE_YAML)
    return path


def test_active_connectors_includes_only_enabled_with_module(tmp_path):
    registry = ConnectorRegistry(config_path=_write_config(tmp_path))
    active = registry.active_connectors()
    assert set(active) == {"linkedin"}
    assert isinstance(active["linkedin"], LinkedInConnector)


def test_disabled_connector_is_not_instantiated(tmp_path):
    registry = ConnectorRegistry(config_path=_write_config(tmp_path))
    assert "freehire" not in registry.active_connectors()


def test_blocked_source_is_retrievable_without_instantiation(tmp_path):
    registry = ConnectorRegistry(config_path=_write_config(tmp_path))
    blocked = registry.blocked_sources()
    assert len(blocked) == 1
    assert blocked[0].name == "buscojobs"
    assert "robots.txt" in blocked[0].blocked_reason
    assert "buscojobs" not in registry.active_connectors()


def test_editing_the_file_changes_the_next_load(tmp_path):
    config_path = _write_config(tmp_path)
    registry = ConnectorRegistry(config_path=config_path)
    assert set(registry.active_connectors()) == {"linkedin"}

    config_path.write_text(FIXTURE_YAML.replace("enabled: false\n    module", "enabled: true\n    module"))
    reloaded = ConnectorRegistry(config_path=config_path)
    assert set(reloaded.active_connectors()) == {"linkedin", "freehire"}


def test_default_config_loads_with_three_active_and_three_blocked():
    registry = ConnectorRegistry()
    active = registry.active_connectors()
    blocked = {b.name for b in registry.blocked_sources()}
    assert set(active) == {"linkedin", "freehire", "computrabajo"}
    assert blocked == {"buscojobs", "indeed_uy", "getonbrd"}


def test_default_config_path_points_at_repo_config():
    assert DEFAULT_CONFIG_PATH.name == "sources.yaml"
