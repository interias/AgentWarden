from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from agent_warden.models import AgentSessionStatus, AgentState, WatcherSnapshot


def make_session(state: AgentState) -> AgentSessionStatus:
    return AgentSessionStatus(
        agent="codex",
        session_id=state.value,
        path=Path(f"{state.value}.jsonl"),
        last_modified=datetime.now(timezone.utc),
        state=state,
    )


def test_empty_snapshot_is_unknown() -> None:
    snapshot = WatcherSnapshot()

    assert snapshot.aggregate_state is AgentState.UNKNOWN


def test_aggregate_state_uses_priority_order() -> None:
    snapshot = WatcherSnapshot(
        sessions=(
            make_session(AgentState.FINISHED),
            make_session(AgentState.ACTIVE),
            make_session(AgentState.FAILED),
        )
    )

    assert snapshot.aggregate_state is AgentState.FAILED


def test_counts_by_state() -> None:
    snapshot = WatcherSnapshot(
        sessions=(
            make_session(AgentState.ACTIVE),
            make_session(AgentState.ACTIVE),
            make_session(AgentState.IDLE),
        )
    )

    counts = snapshot.counts_by_state()

    assert counts[AgentState.ACTIVE] == 2
    assert counts[AgentState.IDLE] == 1
    assert counts[AgentState.FAILED] == 0
