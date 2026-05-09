from __future__ import annotations

import tkinter as tk

from agent_warden.config import AppConfig
from agent_warden.models import AgentState, WatcherSnapshot
from agent_warden.overlay.positioning import (
    DEFAULT_OVERLAY_HEIGHT,
    DEFAULT_OVERLAY_WIDTH,
    calculate_overlay_geometry,
)
from agent_warden.overlay.summary import build_overlay_summary
from agent_warden.watchers.base import AgentWatcher


STATE_COLORS = {
    AgentState.ACTIVE: "#2ecc71",
    AgentState.IDLE: "#f1c40f",
    AgentState.FINISHED: "#3498db",
    AgentState.FAILED: "#e74c3c",
    AgentState.NEEDS_ATTENTION: "#e67e22",
    AgentState.UNKNOWN: "#95a5a6",
}


class TkinterOverlay:
    def __init__(self, config: AppConfig, watcher: AgentWatcher) -> None:
        self.config = config
        self.watcher = watcher
        self._drag_offset_x = 0
        self._drag_offset_y = 0

        self.root = tk.Tk()
        self.root.title("Agent Warden")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", config.overlay_opacity)
        self.root.geometry(self._initial_geometry())
        self.root.configure(bg="#111418")
        self.root.resizable(False, False)

        self.status_label = tk.Label(
            self.root,
            text="Agent Warden",
            fg="#f4f6f8",
            bg="#111418",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=12, pady=(10, 0))

        self.detail_label = tk.Label(
            self.root,
            text="Scanning...",
            fg="#c8d0d8",
            bg="#111418",
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.detail_label.pack(fill="x", padx=12, pady=(3, 0))

        self.root.bind("<ButtonPress-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._drag)
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

    def run(self) -> None:
        self._refresh()
        self.root.mainloop()

    def _initial_geometry(self) -> str:
        geometry = calculate_overlay_geometry(
            position=self.config.overlay_position,
            margin_x=self.config.overlay_x,
            margin_y=self.config.overlay_y,
            width=DEFAULT_OVERLAY_WIDTH,
            height=DEFAULT_OVERLAY_HEIGHT,
            screen_width=self.root.winfo_screenwidth(),
            screen_height=self.root.winfo_screenheight(),
        )
        return geometry.as_tk_geometry()

    def _refresh(self) -> None:
        try:
            self.root.attributes("-topmost", True)
            snapshot = self.watcher.scan()
            self._render(snapshot)
        except Exception as exc:  # pragma: no cover - defensive UI guard
            self._render_error(exc)

        delay_ms = self.config.poll_interval_seconds * 1000
        self.root.after(delay_ms, self._refresh)

    def _render(self, snapshot: WatcherSnapshot) -> None:
        summary = build_overlay_summary(snapshot)
        self.status_label.configure(text=summary.headline, fg=STATE_COLORS[summary.state])
        self.detail_label.configure(text=summary.detail)

    def _render_error(self, exc: Exception) -> None:
        self.status_label.configure(text="Codex: unknown", fg=STATE_COLORS[AgentState.UNKNOWN])
        self.detail_label.configure(text=exc.__class__.__name__)

    def _start_drag(self, event: tk.Event) -> None:
        self._drag_offset_x = event.x
        self._drag_offset_y = event.y

    def _drag(self, event: tk.Event) -> None:
        x = self.root.winfo_pointerx() - self._drag_offset_x
        y = self.root.winfo_pointery() - self._drag_offset_y
        self.root.geometry(f"+{x}+{y}")
