# Map Software

## UML / StarUML

UML is a first-class project artifact. The `uml/` directory contains use-case, class, sequence,
and activity diagrams tied to the actual Python classes and methods. 


## Project purpose

**Map Software is a software-engineering/UML project designed to demonstrate object-oriented analysis, design, and implementation using StarUML.**

The Python implementation is a small working prototype of the design. It processes a video with a monocular camera, estimates relative camera motion from visual features, accumulates those motions into a trajectory, and visualizes the trajectory.

The project **does not implement full SLAM** and does not claim to build a metric map of an environment.

### What the prototype does

1. Accepts a path to a video file.
2. Reads pairs of frames at a configurable interval.
3. Detects ORB visual features.
4. Matches features between frames.
5. Estimates relative camera rotation and translation direction.
6. Accumulates the relative motion into a camera trajectory.
7. Stores the trajectory as nodes and transformations in a graph.
8. Plots the estimated X/Y trajectory.

### What it does not do

- It does not perform loop-closure detection.
- It does not optimize a pose graph.
- It does not reconstruct 3-D landmarks.
- It does not perform bundle adjustment.
- It does not recover absolute metric scale from a monocular video.
- It does not produce a complete environmental map.

The term **trajectory estimation** is therefore used throughout the project instead of **SLAM** or **map generation**.

## Why StarUML matters

The main academic/software-engineering objective is the relationship between:

**requirements → UML model → object-oriented design → implementation**

The UML artifacts should describe the responsibilities and interactions of the classes in `src/map_software/`. See [`docs/UML.md`](docs/UML.md).


## Project structure

```text
Map-Software/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── LIMITATIONS.md
│   └── UML.md
├── examples/
│   └── README.md
├── src/
│   └── map_software/
│       ├── __init__.py
│       ├── feature_extractor.py
│       ├── graph.py
│       ├── robot.py
│       ├── sensor.py
│       ├── user.py
│       └── visual_odometry.py
├── tests/
│   ├── test_graph.py
│   └── test_robot.py
├── uml/
│   └── README.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

## Running the prototype

From the repository root:

```bash
python -m src.map_software.visual_odometry path/to/video.mp4
```

The program prints progress information and displays the estimated camera trajectory.

Camera intrinsics can be supplied with:

```bash
python -m src.map_software.visual_odometry video.mp4 --fx 1000 --fy 1000 --cx 640 --cy 360
```

If calibration is not supplied, the program uses configurable default values. Those defaults are only suitable for demonstration and should not be interpreted as calibrated camera parameters.

## Testing

Run:

```bash
python -m unittest discover -s tests -v
```

The included tests focus on deterministic software components rather than claiming that a particular computer-vision trajectory is ground truth.

## Project status

**Status: educational prototype / software-design demonstration.**

The implementation is intentionally modest. Its value for this project is demonstrating a coherent object-oriented design and its translation into working Python code, rather than presenting a production-grade robotics or SLAM system.
