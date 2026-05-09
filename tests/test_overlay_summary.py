from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from agent_warden.models import AgentSessionStatus, AgentState, WatcherSnapshot
from agent_warden.overlay.summary import build_overlay_summary


def make_session(state: AgentState, session_id: str | None = None) -> AgentSessionStatus:
    return AgentSessionStatus(
        agent="codex",
        session_id=session_id or state.value,
        path=Path(f"{session_id or state.value}.jsonl"),
        last_modified=datetime.now(timezone.utc),
        state=state,
    )


def test_overlay_summary_for_empty_snapshot() -> None:
    summary = build_overlay_summary(WatcherSnapshot())

    assert summary.state is AgentState.UNKNOWN
    assert summary.headline == "Codex: unknown"
    assert summary.detail == "No sessions found"


def test_overlay_summary_prioritizes_current_sessions() -> None:
    snapshot = WatcherSnapshot(
        sessions=(
            make_session(AgentState.ACTIVE, "active-1"),
            make_session(AgentState.ACTIVE, "active-2"),
            make_session(AgentState.IDLE, "idle-1"),
            make_session(AgentState.FINISHED, "old-1"),
            make_session(AgentState.FINISHED, "old-2"),
        )
    )

    summary = build_overlay_summary(snapshot)

    assert summary.state is AgentState.ACTIVE
    assert summary.headline == "Codex: active"
    assert summary.detail == "2 active / 1 idle / 3 current"


def test_overlay_summary_surfaces_attention_before_active() -> None:
    snapshot = WatcherSnapshot(
        sessions=(
            make_session(AgentState.NEEDS_ATTENTION, "attention-1"),
            make_session(AgentState.ACTIVE, "active-1"),
            make_session(AgentState.FINISHED, "old-1"),
        )
    )

    summary = build_overlay_summary(snapshot)

    assert summary.state is AgentState.NEEDS_ATTENTION
    assert summary.detail == "1 attention / 1 active / 2 current"


def test_overlay_summary_when_only_finished_sessions_exist() -> None:
    snapshot = WatcherSnapshot(
        sessions=(
            make_session(AgentState.FINISHED, "old-1"),
            make_session(AgentState.FINISHED, "old-2"),
        )
    )

    summary = build_overlay_summary(snapshot)

    assert summary.state is AgentState.FINISHED
    assert summary.headline == "Codex: finished"
    assert summary.detail == "2 finished"
