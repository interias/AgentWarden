from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path


class AgentState(str, Enum):
    ACTIVE = "active"
    IDLE = "idle"
    FINISHED = "finished"
    FAILED = "failed"
    NEEDS_ATTENTION = "needs_attention"
    UNKNOWN = "unknown"


STATE_PRIORITY: tuple[AgentState, ...] = (
    AgentState.FAILED,
    AgentState.NEEDS_ATTENTION,
    AgentState.ACTIVE,
    AgentState.IDLE,
    AgentState.FINISHED,
    AgentState.UNKNOWN,
)


@dataclass(frozen=True)
class AgentSessionStatus:
    agent: str
    session_id: str
    path: Path
    last_modified: datetime
    state: AgentState
    workspace_name: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class WatcherSnapshot:
    sessions: tuple[AgentSessionStatus, ...] = field(default_factory=tuple)
    scanned_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def aggregate_state(self) -> AgentState:
        if not self.sessions:
            return AgentState.UNKNOWN

        states = {session.state for session in self.sessions}
        for state in STATE_PRIORITY:
            if state in states:
                return state
        return AgentState.UNKNOWN

    def counts_by_state(self) -> dict[AgentState, int]:
        counts = {state: 0 for state in AgentState}
        for session in self.sessions:
            counts[session.state] += 1
        return counts
