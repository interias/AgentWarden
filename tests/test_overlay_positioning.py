from __future__ import annotations

import pytest

from agent_warden.overlay.positioning import calculate_overlay_geometry


@pytest.mark.parametrize(
    ("position", "expected_x", "expected_y"),
    [
        ("top-left", 24, 16),
        ("top-right", 516, 16),
        ("bottom-left", 24, 512),
        ("bottom-right", 516, 512),
    ],
)
def test_calculate_overlay_geometry_for_fixed_positions(
    position: str,
    expected_x: int,
    expected_y: int,
) -> None:
    geometry = calculate_overlay_geometry(
        position=position,
        margin_x=24,
        margin_y=16,
        width=260,
        height=72,
        screen_width=800,
        screen_height=600,
    )

    assert geometry.as_tk_geometry() == f"260x72+{expected_x}+{expected_y}"


def test_calculate_overlay_geometry_clamps_to_screen() -> None:
    geometry = calculate_overlay_geometry(
        position="top-right",
        margin_x=24,
        margin_y=16,
        width=260,
        height=72,
        screen_width=100,
        screen_height=100,
    )

    assert geometry.x == 0
    assert geometry.y == 16


def test_calculate_overlay_geometry_rejects_unknown_position() -> None:
    with pytest.raises(ValueError, match="position"):
        calculate_overlay_geometry(
            position="center",
            margin_x=24,
            margin_y=16,
            width=260,
            height=72,
            screen_width=800,
            screen_height=600,
        )
