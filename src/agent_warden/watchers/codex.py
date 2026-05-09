from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from agent_warden.config import DEFAULT_ACTIVE_THRESHOLD_SECONDS, default_codex_sessions_root
from agent_warden.models import AgentSessionStatus, AgentState, WatcherSnapshot

CODEX_AGENT_NAME = "codex"
DEFAULT_FINISHED_THRESHOLD_SECONDS = 6 * 60 * 60


class CodexWatcher:
    agent_name = CODEX_AGENT_NAME

    def __init__(
        self,
        root: Path | None = None,
        active_threshold_seconds: int = DEFAULT_ACTIVE_THRESHOLD_SECONDS,
        finished_threshold_seconds: int = DEFAULT_FINISHED_THRESHOLD_SECONDS,
    ) -> None:
        if active_threshold_seconds <= 0:
            raise ValueError("active_threshold_seconds must be greater than zero")
        if finished_threshold_seconds <= active_threshold_seconds:
            raise ValueError("finished_threshold_seconds must be greater than active threshold")

        self.root = Path(root).expanduser() if root is not None else default_codex_sessions_root()
        self.active_threshold_seconds = int(active_threshold_seconds)
        self.finished_threshold_seconds = int(finished_threshold_seconds)

    def scan(self) -> WatcherSnapshot:
        scanned_at = datetime.now(timezone.utc)
        if not self.root.exists() or not self.root.is_dir():
            return WatcherSnapshot(sessions=(), scanned_at=scanned_at)

        sessions: list[AgentSessionStatus] = []
        try:
            candidates = sorted(self.root.rglob("*.jsonl"), key=lambda path: str(path).lower())
        except OSError:
            return WatcherSnapshot(sessions=(), scanned_at=scanned_at)

        for path in candidates:
            try:
                stat_result = path.stat()
            except OSError:
                continue

            last_modified = datetime.fromtimestamp(stat_result.st_mtime, tz=timezone.utc)
            state, reason = self._infer_state(last_modified=last_modified, now=scanned_at)
            sessions.append(
                AgentSessionStatus(
                    agent=CODEX_AGENT_NAME,
                    session_id=self._session_id_from_path(path),
                    path=path,
                    last_modified=last_modified,
                    state=state,
                    workspace_name=self._workspace_name_from_path(path),
                    reason=reason,
                )
            )

        sessions.sort(key=lambda session: session.last_modified, reverse=True)
        return WatcherSnapshot(sessions=tuple(sessions), scanned_at=scanned_at)

    def _infer_state(
        self,
        last_modified: datetime,
        now: datetime,
    ) -> tuple[AgentState, str]:
        age_seconds = (now - last_modified).total_seconds()
        if age_seconds <= self.active_threshold_seconds:
            return AgentState.ACTIVE, "recently modified"
        if age_seconds >= self.finished_threshold_seconds:
            return AgentState.FINISHED, "not modified for several hours"
        return AgentState.IDLE, "not recently modified"

    @staticmethod
    def _session_id_from_path(path: Path) -> str:
        return path.stem

    def _workspace_name_from_path(self, path: Path) -> str | None:
        try:
            relative = path.relative_to(self.root)
        except ValueError:
            return None

        # Codex currently stores date-like folders under sessions. Do not infer
        # workspace names from session file content in the privacy-first MVP.
        parts = relative.parts[:-1]
        if len(parts) >= 2 and parts[0].lower() in {"workspace", "workspaces", "project", "projects"}:
            return parts[1]
        return None
