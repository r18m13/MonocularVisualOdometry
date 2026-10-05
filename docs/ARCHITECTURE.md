# Architecture

## Architectural goal

The architecture is intentionally small. It demonstrates separation of responsibilities so that the classes can be represented clearly in a StarUML class diagram.

## Components

### `User`

Responsible for collecting the user's request/data source.

### `Sensor`

Represents the visual data source. In the implementation this is a video path rather than a physical sensor driver.

### `FeatureExtractor`

Responsible for computer-vision processing of two frames:

- ORB feature detection
- descriptor matching
- essential-matrix estimation
- relative rotation/translation recovery

It does not maintain application state.

### `Robot`

Represents the moving camera and maintains its current homogeneous pose. Despite the original project using the name `Robot`, the implementation should be understood as a camera-motion abstraction.

### `Graph`

Stores estimated poses and relative transformations. It is a trajectory data structure. It does **not** optimize the graph.

### `VisualOdometrySystem`

Coordinates the application workflow:

```text
Video
  ↓
Sensor / video source
  ↓
VisualOdometrySystem
  ↓
FeatureExtractor
  ↓
Relative camera transform
  ↓
Robot
  ↓
Graph + trajectory
  ↓
Trajectory visualization
```

## Dependencies

`VisualOdometrySystem` depends on the other domain/application classes. The lower-level classes do not depend on the application coordinator.

## Design principle

The implementation separates:

- input acquisition,
- visual measurement,
- pose state,
- trajectory storage,
- application orchestration.

This separation is the primary software-engineering result of the project.
