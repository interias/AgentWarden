from __future__ import annotations

from dataclasses import dataclass

from agent_warden.config import OVERLAY_POSITIONS


DEFAULT_OVERLAY_WIDTH = 260
DEFAULT_OVERLAY_HEIGHT = 72


@dataclass(frozen=True)
class OverlayGeometry:
    width: int
    height: int
    x: int
    y: int

    def as_tk_geometry(self) -> str:
        return f"{self.width}x{self.height}+{self.x}+{self.y}"


def calculate_overlay_geometry(
    *,
    position: str,
    margin_x: int,
    margin_y: int,
    width: int,
    height: int,
    screen_width: int,
    screen_height: int,
) -> OverlayGeometry:
    normalized_position = position.lower().replace("_", "-")
    if normalized_position not in OVERLAY_POSITIONS:
        raise ValueError(f"position must be one of: {', '.join(OVERLAY_POSITIONS)}")
    if margin_x < 0 or margin_y < 0:
        raise ValueError("margins must be zero or greater")

    if normalized_position.endswith("right"):
        x = screen_width - width - margin_x
    else:
        x = margin_x

    if normalized_position.startswith("bottom"):
        y = screen_height - height - margin_y
    else:
        y = margin_y

    return OverlayGeometry(
        width=width,
        height=height,
        x=max(0, x),
        y=max(0, y),
    )
