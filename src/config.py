from typing import Tuple

# Window / Camera
WINDOW_WIDTH: int = 1680
WINDOW_HEIGHT: int = 1050
CAMERA_ID: int = 0

# Illusion scale (centimeters)
SCREEN_WIDTH_CM: float = 30.0
# Keep SCREEN_HEIGHT_CM consistent with aspect ratio
SCREEN_HEIGHT_CM: float = SCREEN_WIDTH_CM * (WINDOW_HEIGHT / WINDOW_WIDTH)
DEFAULT_VIEWER_Z_CM: float = 60.0

# Colors (RGB / RGBA floats)
NEON_GREEN: Tuple[float, float, float] = (0.0, 1.0, 0.53)
DARK_BG: Tuple[float, float, float, float] = (0.05, 0.05, 0.05, 1.0)
GRID_COLOR: Tuple[float, float, float] = (0.3, 0.3, 0.3)

__all__ = [
    "WINDOW_WIDTH",
    "WINDOW_HEIGHT",
    "CAMERA_ID",
    "SCREEN_WIDTH_CM",
    "SCREEN_HEIGHT_CM",
    "DEFAULT_VIEWER_Z_CM",
    "NEON_GREEN",
    "DARK_BG",
    "GRID_COLOR",
]
