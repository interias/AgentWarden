from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

MIN_POLL_INTERVAL_SECONDS = 5
MAX_POLL_INTERVAL_SECONDS = 60
DEFAULT_POLL_INTERVAL_SECONDS = 10
DEFAULT_ACTIVE_THRESHOLD_SECONDS = 60
DEFAULT_OVERLAY_POSITION = "top-right"
OVERLAY_POSITIONS = ("top-left", "top-right", "bottom-left", "bottom-right")


def default_codex_sessions_root() -> Path:
    return Path.home() / ".codex" / "sessions"


def default_config_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "AgentWarden" / "config.json"
    return Path.home() / ".agent-warden" / "config.json"


@dataclass(frozen=True)
class AppConfig:
    poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS
    codex_sessions_root: Path = field(default_factory=default_codex_sessions_root)
    active_threshold_seconds: int = DEFAULT_ACTIVE_THRESHOLD_SECONDS
    overlay_x: int = 24
    overlay_y: int = 24
    overlay_opacity: float = 0.92
    overlay_position: str = DEFAULT_OVERLAY_POSITION

    def __post_init__(self) -> None:
        poll_interval = int(self.poll_interval_seconds)
        active_threshold = int(self.active_threshold_seconds)
        opacity = float(self.overlay_opacity)
        overlay_x = int(self.overlay_x)
        overlay_y = int(self.overlay_y)
        overlay_position = str(self.overlay_position).lower().replace("_", "-")

        if not MIN_POLL_INTERVAL_SECONDS <= poll_interval <= MAX_POLL_INTERVAL_SECONDS:
            raise ValueError(
                "poll_interval_seconds must be between "
                f"{MIN_POLL_INTERVAL_SECONDS} and {MAX_POLL_INTERVAL_SECONDS}"
            )
        if active_threshold <= 0:
            raise ValueError("active_threshold_seconds must be greater than zero")
        if overlay_x < 0 or overlay_y < 0:
            raise ValueError("overlay_x and overlay_y must be zero or greater")
        if not 0.2 <= opacity <= 1.0:
            raise ValueError("overlay_opacity must be between 0.2 and 1.0")
        if overlay_position not in OVERLAY_POSITIONS:
            raise ValueError(f"overlay_position must be one of: {', '.join(OVERLAY_POSITIONS)}")

        object.__setattr__(self, "poll_interval_seconds", poll_interval)
        object.__setattr__(self, "codex_sessions_root", Path(self.codex_sessions_root).expanduser())
        object.__setattr__(self, "active_threshold_seconds", active_threshold)
        object.__setattr__(self, "overlay_x", overlay_x)
        object.__setattr__(self, "overlay_y", overlay_y)
        object.__setattr__(self, "overlay_opacity", opacity)
        object.__setattr__(self, "overlay_position", overlay_position)

    @classmethod
    def load(cls, path: Path | None = None) -> "AppConfig":
        config_path = path or default_config_path()
        if not config_path.exists():
            return cls()

        with config_path.open("r", encoding="utf-8-sig") as handle:
            raw = json.load(handle)
        if not isinstance(raw, dict):
            raise ValueError("Config file must contain a JSON object")
        return cls.from_mapping(raw)

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "AppConfig":
        known_keys = {
            "poll_interval_seconds",
            "codex_sessions_root",
            "active_threshold_seconds",
            "overlay_x",
            "overlay_y",
            "overlay_opacity",
            "overlay_position",
        }
        values = {key: raw[key] for key in known_keys if key in raw}
        if "codex_sessions_root" in values:
            values["codex_sessions_root"] = Path(values["codex_sessions_root"]).expanduser()
        return cls(**values)

    def with_overrides(
        self,
        *,
        poll_interval_seconds: int | None = None,
        codex_sessions_root: Path | None = None,
        active_threshold_seconds: int | None = None,
        overlay_opacity: float | None = None,
        overlay_position: str | None = None,
    ) -> "AppConfig":
        values: dict[str, Any] = {}
        if poll_interval_seconds is not None:
            values["poll_interval_seconds"] = poll_interval_seconds
        if codex_sessions_root is not None:
            values["codex_sessions_root"] = codex_sessions_root
        if active_threshold_seconds is not None:
            values["active_threshold_seconds"] = active_threshold_seconds
        if overlay_opacity is not None:
            values["overlay_opacity"] = overlay_opacity
        if overlay_position is not None:
            values["overlay_position"] = overlay_position
        if not values:
            return self
        return replace(self, **values)
