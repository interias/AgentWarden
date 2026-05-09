from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .config import AppConfig, OVERLAY_POSITIONS
from .models import AgentSessionStatus, WatcherSnapshot
from .overlay.tkinter_overlay import TkinterOverlay
from .watchers.codex import CodexWatcher


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-warden",
        description="Monitor local AI coding agent activity with a small overlay.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Optional path to a JSON config file.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Print one metadata-only status scan instead of opening the overlay.",
    )
    parser.add_argument(
        "--sessions-root",
        type=Path,
        help="Override the Codex sessions root for this run.",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        help="Override polling interval in seconds. Valid range: 5-60.",
    )
    parser.add_argument(
        "--active-threshold",
        type=int,
        help="Override seconds since last modification considered active.",
    )
    parser.add_argument(
        "--opacity",
        type=float,
        help="Override overlay opacity for this run. Valid range: 0.2-1.0.",
    )
    parser.add_argument(
        "--position",
        choices=OVERLAY_POSITIONS,
        help="Override overlay position for this run.",
    )
    return parser


def create_codex_watcher(config: AppConfig) -> CodexWatcher:
    return CodexWatcher(
        root=config.codex_sessions_root,
        active_threshold_seconds=config.active_threshold_seconds,
    )


def format_snapshot(snapshot: WatcherSnapshot) -> str:
    if not snapshot.sessions:
        return "No Codex sessions found."

    lines = [
        f"Scanned {len(snapshot.sessions)} Codex session(s).",
        f"Aggregate state: {snapshot.aggregate_state.value}",
    ]
    for session in snapshot.sessions[:10]:
        lines.append(format_session(session))
    if len(snapshot.sessions) > 10:
        lines.append(f"... {len(snapshot.sessions) - 10} more session(s) omitted.")
    return "\n".join(lines)


def format_session(session: AgentSessionStatus) -> str:
    workspace = f" workspace={session.workspace_name}" if session.workspace_name else ""
    return (
        f"- {session.agent}:{session.session_id} "
        f"state={session.state.value}{workspace} "
        f"modified={session.last_modified.isoformat()}"
    )


def run(
    config_path: Path | None = None,
    once: bool = False,
    sessions_root: Path | None = None,
    poll_interval_seconds: int | None = None,
    active_threshold_seconds: int | None = None,
    overlay_opacity: float | None = None,
    overlay_position: str | None = None,
) -> int:
    config = AppConfig.load(config_path).with_overrides(
        codex_sessions_root=sessions_root,
        poll_interval_seconds=poll_interval_seconds,
        active_threshold_seconds=active_threshold_seconds,
        overlay_opacity=overlay_opacity,
        overlay_position=overlay_position,
    )
    watcher = create_codex_watcher(config)

    if once:
        print(format_snapshot(watcher.scan()))
        return 0

    overlay = TkinterOverlay(config=config, watcher=watcher)
    overlay.run()
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(
        config_path=args.config,
        once=args.once,
        sessions_root=args.sessions_root,
        poll_interval_seconds=args.poll_interval,
        active_threshold_seconds=args.active_threshold,
        overlay_opacity=args.opacity,
        overlay_position=args.position,
    )
