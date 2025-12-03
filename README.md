# Holographic 

A real-time 3D holographic visualization system that responds to your head position and eye gaze using face tracking.

## Features

- **Eye Tracking**: Uses MediaPipe FaceMesh to track your eyes in real-time
- **Head-Based Perspective**: Creates an off-axis frustum 3D view that adjusts based on your head position
- **Interactive 3D Graphics**: Renders animated 3D objects (cubes, octahedrons, grids) using OpenGL
- **Calibration**: Press 'C' to calibrate the eye tracking to your current position
- **Smooth Motion**: Exponential smoothing for fluid head movement tracking

## Requirements

- Python 3.7+
- Webcam
- Dependencies listed in `req.txt`:
  - opencv-python
  - mediapipe
  - numpy
  - pygame
  - PyOpenGL
  - PyOpenGL_accelerate

## Installation
```bash
python3.11 -m venv myenv
```

mediapipe works best on python 3.11

```bash
pip install -r req.txt
```

## Usage

```bash
python main.py [--camera CAMERA_ID]
```

**Controls:**
- Press **C** to calibrate (point your face straight at the camera)
- Press **ESC** to quit

## How It Works

1. **FaceTracker** (`src/tracker.py`): Captures video from your webcam and detects eye position using MediaPipe
2. **IllusionScene** (`src/scene.py`): Renders 3D graphics with an off-axis projection that shifts based on eye position
3. **Config** (`src/config.py`): Configuration constants for window size, colors, and camera settings

The result is a parallax 3D effect where the scene appears to move based on where you're looking.

## Project Structure

```
├── main.py          # Entry point
├── req.txt          # Dependencies
└── src/
    ├── config.py    # Configuration constants
    ├── tracker.py   # Face and eye tracking
    └── scene.py     # 3D graphics rendering
```
