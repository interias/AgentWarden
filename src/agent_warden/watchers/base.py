from __future__ import annotations

from typing import Protocol

from agent_warden.models import WatcherSnapshot


class AgentWatcher(Protocol):
    agent_name: str

    def scan(self) -> WatcherSnapshot:
        """Return the current metadata-only view of watched agent sessions."""
