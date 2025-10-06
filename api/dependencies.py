"""Dependency injection helpers for the FastAPI app."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import Depends

from core.config_store import ConfigStore
from core.dhcp_assigner import DHCPAssigner
from core.script_pusher import ScriptPusher
from core.topology_store import TopologyRepository
from models import APISettings


@lru_cache
def get_settings() -> APISettings:
    """Return application settings (cached for process lifetime)."""

    return APISettings()  # type: ignore[call-arg]


def get_config_store(settings: APISettings = Depends(get_settings)) -> ConfigStore:
    return ConfigStore.from_path(settings.config_path)


def get_script_pusher(settings: APISettings = Depends(get_settings)) -> ScriptPusher:
    return ScriptPusher(scripts_base_dir=settings.scripts_dir)


def get_dhcp_assigner(config_store: ConfigStore = Depends(get_config_store)) -> DHCPAssigner:
    return DHCPAssigner(config_store)


@lru_cache(maxsize=None)
def _topology_repository_factory(storage_dir: str) -> TopologyRepository:
    return TopologyRepository(Path(storage_dir))


def get_topology_repository(settings: APISettings = Depends(get_settings)) -> TopologyRepository:
    return _topology_repository_factory(str(settings.topologies_dir))
