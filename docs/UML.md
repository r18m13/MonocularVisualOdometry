# UML / StarUML Specification

## Purpose

The UML model is the primary design artifact for this project. It should communicate the system before the implementation is considered.


## Use-case diagram

### Actor

**User**

### Use cases

- Provide video source
- Process video
- Estimate camera motion
- View trajectory

Relationships:

```text
User
 ├──> Provide video source
 ├──> Process video
 └──> View trajectory

Process video
 └── <<include>> Estimate camera motion
```

## Class diagram

Classes:

```text
User
Sensor
VisualOdometrySystem
FeatureExtractor
Robot
Graph
```

Key relationships:

```text
VisualOdometrySystem o-- Sensor
VisualOdometrySystem o-- FeatureExtractor
VisualOdometrySystem o-- Robot
VisualOdometrySystem o-- Graph

VisualOdometrySystem --> FeatureExtractor : requests relative pose
VisualOdometrySystem --> Robot : updates pose
VisualOdometrySystem --> Graph : stores trajectory
```

### Responsibilities

| Class | Responsibility |
|---|---|
| `User` | Captures the user's request/data source |
| `Sensor` | Represents/acquires the video data source |
| `FeatureExtractor` | Estimates relative motion from two frames |
| `Robot` | Maintains the current camera pose |
| `Graph` | Stores poses and transformations |
| `VisualOdometrySystem` | Coordinates the processing workflow |

## Sequence diagram

The principal interaction is:

```text
User -> VisualOdometrySystem : process(video)
VisualOdometrySystem -> Sensor : acquire_data
VisualOdometrySystem -> FeatureExtractor : extract_features(frame0, frame1)
FeatureExtractor --> VisualOdometrySystem : rotation, translation
VisualOdometrySystem -> Robot : update_pose(transform)
Robot --> VisualOdometrySystem : current pose
VisualOdometrySystem -> Graph : add_node()
VisualOdometrySystem -> Graph : add_edge()
VisualOdometrySystem --> User : trajectory visualization
```

## State/activity perspective

A useful activity diagram is:

```text
Start
  ↓
Open video
  ↓
Read two frames
  ↓
Enough visual information?
  ├── No → Advance frame interval → Read two frames
  └── Yes
       ↓
Estimate relative pose
       ↓
Accumulate camera pose
       ↓
Store trajectory
       ↓
More frames?
  ├── Yes → Read two frames
  └── No
       ↓
Plot trajectory
       ↓
End
```
