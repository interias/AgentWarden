from __future__ import annotations

import os
import time

from agent_warden.app import main


def test_once_command_accepts_runtime_overrides(tmp_path, capsys) -> None:
    session_file = tmp_path / "session.jsonl"
    session_file.write_text("{}\n", encoding="utf-8")
    now = time.time()
    os.utime(session_file, (now, now))

    exit_code = main(
        [
            "--once",
            "--sessions-root",
            str(tmp_path),
            "--poll-interval",
            "5",
            "--active-threshold",
            "60",
            "--opacity",
            "0.9",
            "--position",
            "bottom-right",
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Scanned 1 Codex session(s)." in output
    assert "state=active" in output
