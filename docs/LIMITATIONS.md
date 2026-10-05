# Limitations

This is an educational prototype, not a production robotics system.

## Computer vision

- ORB matching can fail on low-texture, blurred, or highly repetitive scenes.
- The system uses simple descriptor matching rather than a more robust feature-tracking pipeline.
- Relative pose quality depends on camera calibration and image quality.

## Monocular geometry

A monocular camera does not provide absolute metric scale from two-view geometry alone. The plotted trajectory therefore has arbitrary scale.

## Trajectory drift

Relative pose estimates are accumulated without loop closure or global optimization. Errors can accumulate over time.

## No environmental map

The implementation stores camera poses but does not reconstruct persistent 3-D landmarks. The output is a trajectory, not a map of the environment.

## No SLAM optimization

There is no pose-graph optimization, bundle adjustment, loop closure, or landmark optimization.

## Camera model

If camera calibration is not provided, the system creates a simple focal-length approximation from image dimensions. This is for demonstration only.

## Input handling

The prototype expects a readable video file and does not implement a GUI, persistent project database, or physical sensor interface.
