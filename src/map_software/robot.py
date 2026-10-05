"""Camera pose accumulation."""


import numpy as np


class Robot:
    """Maintains the current homogeneous camera pose."""

    def __init__(self, pose=None):
        self.pose = np.eye(4) if pose is None else np.asarray(pose, dtype=float)

    def update_pose(self, relative_pose):
        """Apply a relative 4x4 transform to the current pose."""
        relative_pose = np.asarray(relative_pose, dtype=float)
        if relative_pose.shape != (4, 4):
            raise ValueError("relative_pose must be a 4x4 matrix.")
        self.pose = self.pose @ relative_pose
        return self.pose.copy()
