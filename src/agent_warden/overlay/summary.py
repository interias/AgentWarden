from __future__ import annotations

from dataclasses import dataclass

from agent_warden.models import AgentState, WatcherSnapshot


@dataclass(frozen=True)
class OverlaySummary:
    state: AgentState
    headline: str
    detail: str


def build_overlay_summary(snapshot: WatcherSnapshot) -> OverlaySummary:
    counts = snapshot.counts_by_state()
    total = len(snapshot.sessions)
    if total == 0:
        return OverlaySummary(
            state=AgentState.UNKNOWN,
            headline="Codex: unknown",
            detail="No sessions found",
        )

    active = counts[AgentState.ACTIVE]
    idle = counts[AgentState.IDLE]
    failed = counts[AgentState.FAILED]
    needs_attention = counts[AgentState.NEEDS_ATTENTION]
    finished = counts[AgentState.FINISHED]
    unknown = counts[AgentState.UNKNOWN]
    attention = failed + needs_attention
    current = active + idle + attention + unknown

    state = snapshot.aggregate_state
    headline = f"Codex: {state.value.replace('_', ' ')}"

    if attention:
        detail = f"{attention} attention / {active} active / {current} current"
    elif active:
        detail = f"{active} active / {idle} idle / {current} current"
    elif idle:
        detail = f"{idle} idle / {finished} finished"
    elif unknown:
        detail = f"{unknown} unknown / {finished} finished"
    else:
        detail = f"{finished} finished"

    return OverlaySummary(state=state, headline=headline, detail=detail)
