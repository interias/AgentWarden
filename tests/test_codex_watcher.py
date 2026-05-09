from __future__ import annotations

import os
import time

from agent_warden.models import AgentState
from agent_warden.watchers.codex import CodexWatcher


def test_missing_codex_root_returns_empty_snapshot(tmp_path) -> None:
    watcher = CodexWatcher(root=tmp_path / "missing")

    snapshot = watcher.scan()

    assert snapshot.sessions == ()
    assert snapshot.aggregate_state is AgentState.UNKNOWN


def test_recent_jsonl_file_is_active(tmp_path) -> None:
    session_file = tmp_path / "2026" / "05" / "09" / "session-1.jsonl"
    session_file.parent.mkdir(parents=True)
    session_file.write_text('{"private":"do not parse"}\n', encoding="utf-8")
    now = time.time()
    os.utime(session_file, (now, now))

    watcher = CodexWatcher(root=tmp_path, active_threshold_seconds=60)
    snapshot = watcher.scan()

    assert len(snapshot.sessions) == 1
    session = snapshot.sessions[0]
    assert session.session_id == "session-1"
    assert session.state is AgentState.ACTIVE
    assert session.reason == "recently modified"


def test_old_jsonl_file_is_not_active(tmp_path) -> None:
    session_file = tmp_path / "session-old.jsonl"
    session_file.write_text("{}\n", encoding="utf-8")
    old_time = time.time() - 120
    os.utime(session_file, (old_time, old_time))

    watcher = CodexWatcher(
        root=tmp_path,
        active_threshold_seconds=60,
        finished_threshold_seconds=3600,
    )
    snapshot = watcher.scan()

    assert len(snapshot.sessions) == 1
    assert snapshot.sessions[0].state is AgentState.IDLE


def test_very_old_jsonl_file_is_finished(tmp_path) -> None:
    session_file = tmp_path / "session-finished.jsonl"
    session_file.write_text("{}\n", encoding="utf-8")
    old_time = time.time() - 7200
    os.utime(session_file, (old_time, old_time))

    watcher = CodexWatcher(
        root=tmp_path,
        active_threshold_seconds=60,
        finished_threshold_seconds=3600,
    )
    snapshot = watcher.scan()

    assert snapshot.sessions[0].state is AgentState.FINISHED


def test_watcher_does_not_return_prompt_contents(tmp_path) -> None:
    private_text = "PRIVATE_PROMPT_CONTENT_SHOULD_NOT_LEAK"
    session_file = tmp_path / "session-private.jsonl"
    session_file.write_text(f'{{"prompt":"{private_text}"}}\n', encoding="utf-8")

    watcher = CodexWatcher(root=tmp_path)
    snapshot = watcher.scan()

    rendered = repr(snapshot)
    assert private_text not in rendered
