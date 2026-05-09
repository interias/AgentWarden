from __future__ import annotations

import json

import pytest

from agent_warden.config import AppConfig, default_codex_sessions_root


def test_config_defaults() -> None:
    config = AppConfig()

    assert config.poll_interval_seconds == 10
    assert config.codex_sessions_root == default_codex_sessions_root()
    assert config.active_threshold_seconds == 60
    assert config.overlay_opacity == 0.92
    assert config.overlay_position == "top-right"


@pytest.mark.parametrize("interval", [4, 61])
def test_poll_interval_must_be_in_allowed_range(interval: int) -> None:
    with pytest.raises(ValueError, match="poll_interval_seconds"):
        AppConfig(poll_interval_seconds=interval)


def test_load_missing_config_returns_defaults(tmp_path) -> None:
    config = AppConfig.load(tmp_path / "missing.json")

    assert config == AppConfig()


def test_load_config_from_json(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    sessions_root = tmp_path / "sessions"
    config_path.write_text(
        json.dumps(
            {
                "poll_interval_seconds": 5,
                "codex_sessions_root": str(sessions_root),
                "active_threshold_seconds": 30,
                "overlay_x": 10,
                "overlay_y": 20,
                "overlay_opacity": 0.8,
                "overlay_position": "bottom-left",
            }
        ),
        encoding="utf-8",
    )

    config = AppConfig.load(config_path)

    assert config.poll_interval_seconds == 5
    assert config.codex_sessions_root == sessions_root
    assert config.active_threshold_seconds == 30
    assert config.overlay_x == 10
    assert config.overlay_y == 20
    assert config.overlay_opacity == 0.8
    assert config.overlay_position == "bottom-left"


def test_load_config_accepts_utf8_bom(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_bytes(b'\xef\xbb\xbf{"poll_interval_seconds": 5}')

    config = AppConfig.load(config_path)

    assert config.poll_interval_seconds == 5


def test_config_with_overrides_keeps_unspecified_values(tmp_path) -> None:
    sessions_root = tmp_path / "sessions"
    config = AppConfig().with_overrides(
        poll_interval_seconds=5,
        codex_sessions_root=sessions_root,
        active_threshold_seconds=30,
        overlay_opacity=0.75,
        overlay_position="bottom-right",
    )

    assert config.poll_interval_seconds == 5
    assert config.codex_sessions_root == sessions_root
    assert config.active_threshold_seconds == 30
    assert config.overlay_opacity == 0.75
    assert config.overlay_x == 24
    assert config.overlay_y == 24
    assert config.overlay_position == "bottom-right"


def test_config_with_invalid_override_raises() -> None:
    with pytest.raises(ValueError, match="poll_interval_seconds"):
        AppConfig().with_overrides(poll_interval_seconds=1)


def test_config_rejects_invalid_overlay_position() -> None:
    with pytest.raises(ValueError, match="overlay_position"):
        AppConfig(overlay_position="center")
