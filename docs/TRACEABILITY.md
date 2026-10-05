# UML-to-Code Traceability

This table is intended to make the StarUML model and Python implementation easy to compare.

| UML element | Python implementation | Purpose |
|---|---|---|
| User | `src/map_software/user.py` | Captures user input |
| Sensor | `src/map_software/sensor.py` | Represents the video data source |
| FeatureExtractor | `src/map_software/feature_extractor.py` | Estimates relative visual motion |
| Robot | `src/map_software/robot.py` | Maintains camera pose |
| Graph | `src/map_software/graph.py` | Stores poses and transformations |
| VisualOdometrySystem | `src/map_software/visual_odometry.py` | Coordinates the workflow |

The UML class names should match the Python class names exactly. This keeps the StarUML model and implementation traceable.

## Requirement-to-class traceability

| Requirement | Primary class |
|---|---|
| Accept a video source | `User`, `Sensor` |
| Process consecutive frames | `VisualOdometrySystem` |
| Estimate relative camera motion | `FeatureExtractor` |
| Accumulate camera pose | `Robot` |
| Store trajectory information | `Graph` |
| Visualize trajectory | `VisualOdometrySystem` |
