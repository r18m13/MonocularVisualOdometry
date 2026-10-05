# StarUML Model Specification

The UML artifacts in this directory are tied directly to the Python implementation in
`src/map_software/`. The supplied repository did not contain a native StarUML `.mdj` file,
so this specification does not pretend that one existed.

## 1. Use Case Diagram — `Map Software Use Cases`

**Actor**
- `User`

**Use cases**
- `Select video source`
- `Process monocular video`
- `Estimate relative camera motion`
- `Accumulate camera pose`
- `Store trajectory`
- `Visualize estimated trajectory`

**Relationships**
- User -> Select video source
- User -> Process monocular video
- User -> Visualize estimated trajectory
- Process monocular video `<<include>>` Estimate relative camera motion
- Process monocular video `<<include>>` Accumulate camera pose
- Process monocular video `<<include>>` Store trajectory

## 2. Class Diagram — `Map Software Classes`

The class diagram must match the implementation.

### User
- Attributes: `id`, `video_path`
- Operation: `request_data_source()`

### Sensor
- Attributes: `type`, `data`
- Operation: `acquire_data(path)`

### VisualOdometrySystem
- Attributes: `feature_extractor : FeatureExtractor`, `graph : Graph`, `robot : Robot`, `sensor : Sensor`, `trajectory`
- Operations: `process(video_path, frame_interval_seconds)`, `plot_trajectory(positions)`, `_homogeneous_transform(rotation, translation)`

### FeatureExtractor
- Attributes: `camera_matrix`, `nfeatures`
- Operations: `extract_features(frame_0, frame_1)`, `_camera_matrix(frame)`

### Robot
- Attribute: `pose`
- Operation: `update_pose(relative_pose)`

### Graph
- Attribute: `graph : nx.Graph`
- Operations: `add_node(index, pose)`, `add_edge(start, end, transformation)`, `optimize_graph()`

**Relationships**
- `VisualOdometrySystem` composes `FeatureExtractor`, `Graph`, `Robot`, and `Sensor`.
- `User` supplies/selects the input source through the `Sensor` abstraction.
- `VisualOdometrySystem` uses `FeatureExtractor`, `Robot`, and `Graph`.

**Important constraint:** `Graph.optimize_graph()` is deliberately unimplemented and raises
`NotImplementedError`. It must not be modeled as completed graph optimization.

## 3. Sequence Diagram — `Process Video`

1. User -> VisualOdometrySystem: `process(video_path)`
2. VisualOdometrySystem -> Sensor: use video source
3. VisualOdometrySystem -> Graph: `add_node(0, initial_pose)`
4. For each sampled frame pair:
   - VisualOdometrySystem -> FeatureExtractor: `extract_features(frame0, frame1)`
   - FeatureExtractor --> VisualOdometrySystem: `rotation, translation`
   - VisualOdometrySystem -> VisualOdometrySystem: build relative transform
   - VisualOdometrySystem -> Robot: `update_pose(relative)`
   - Robot --> VisualOdometrySystem: current pose
   - VisualOdometrySystem -> Graph: `add_node(...)`
   - VisualOdometrySystem -> Graph: `add_edge(...)`
   - VisualOdometrySystem -> trajectory: append position
5. VisualOdometrySystem --> User: estimated trajectory

## 4. Activity Diagram — `Estimate Camera Trajectory`

Receive video path -> open video -> validate video -> read/validate FPS -> select sampled
frame pair -> extract ORB features -> validate matches -> estimate essential matrix with RANSAC
-> recover pose -> build relative transform -> update pose -> store graph data -> append X/Y
position -> repeat -> release video -> return trajectory.

If feature extraction or pose recovery fails for a frame pair, the implementation skips that pair
and continues.

## Project Scope

This is an **object-oriented software design / StarUML project** with a Python implementation
demonstrating **monocular visual-odometry trajectory estimation**.

It does not claim:
- SLAM
- loop closure
- graph optimization
- bundle adjustment
- landmark mapping
- metric-scale reconstruction
- a complete environmental map
