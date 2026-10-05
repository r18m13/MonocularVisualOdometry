"""Application service for monocular visual-odometry estimation."""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from .feature_extractor import FeatureExtractor
from .graph import Graph
from .robot import Robot
from .sensor import Sensor


class VisualOdometrySystem:
    """Coordinate video processing, pose estimation, and trajectory storage."""

    def __init__(self, feature_extractor=None, graph=None, robot=None):
        self.feature_extractor = feature_extractor or FeatureExtractor()
        self.graph = graph or Graph()
        self.robot = robot or Robot()
        self.sensor = Sensor()
        self.trajectory = [self.robot.pose[:3, 3].copy()]

    @staticmethod
    def _homogeneous_transform(rotation, translation):
        transform = np.eye(4)
        transform[:3, :3] = rotation
        transform[:3, 3] = np.asarray(translation).reshape(3)
        return transform

    def process(self, video_path, frame_interval_seconds=0.2):
        """Estimate and return an array of camera positions."""
        video_path = str(Path(video_path))
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            raise FileNotFoundError(f"Unable to open video: {video_path}")

        fps = capture.get(cv2.CAP_PROP_FPS)
        if not fps or fps <= 0:
            capture.release()
            raise ValueError("The video does not provide a valid frame rate.")

        interval = max(1, int(round(fps * frame_interval_seconds)))
        current_frame = 0
        node_index = 0
        self.graph.add_node(node_index, self.robot.pose.copy())

        try:
            while True:
                capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                ok0, frame0 = capture.read()
                if not ok0:
                    break

                capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame + interval)
                ok1, frame1 = capture.read()
                if not ok1:
                    break

                try:
                    rotation, translation = self.feature_extractor.extract_features(
                        frame0, frame1
                    )
                except ValueError:
                    # A frame pair may lack enough visual information.
                    current_frame += interval
                    continue

                relative = self._homogeneous_transform(rotation, translation)
                previous_index = node_index
                node_index += 1
                pose = self.robot.update_pose(relative)
                self.graph.add_node(node_index, pose.copy())
                self.graph.add_edge(previous_index, node_index, relative)
                self.trajectory.append(pose[:3, 3].copy())
                current_frame += interval
        finally:
            capture.release()

        return np.asarray(self.trajectory)

    def plot_trajectory(self, positions=None):
        """Display the estimated X/Y camera trajectory."""
        positions = self.trajectory if positions is None else positions
        positions = np.asarray(positions)
        if len(positions) == 0:
            raise ValueError("No trajectory positions are available.")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(positions[:, 0], positions[:, 1], "o-", label="Estimated camera trajectory")
        ax.set_xlabel("Estimated X")
        ax.set_ylabel("Estimated Y")
        ax.set_title("Monocular Visual-Odometry Trajectory")
        ax.grid(True)
        ax.legend()
        plt.show()
        return fig, ax


def main():
    parser = argparse.ArgumentParser(
        description="Estimate and plot a camera trajectory from a monocular video."
    )
    parser.add_argument("video", help="Path to the input video.")
    parser.add_argument(
        "--fx", type=float, default=None, help="Camera focal length in pixels (x)."
    )
    parser.add_argument(
        "--fy", type=float, default=None, help="Camera focal length in pixels (y)."
    )
    parser.add_argument(
        "--cx", type=float, default=None, help="Principal point x-coordinate."
    )
    parser.add_argument(
        "--cy", type=float, default=None, help="Principal point y-coordinate."
    )
    args = parser.parse_args()

    camera_matrix = None
    values = (args.fx, args.fy, args.cx, args.cy)
    if any(value is not None for value in values):
        if not all(value is not None for value in values):
            parser.error("Provide all of --fx, --fy, --cx, and --cy together.")
        camera_matrix = np.array(
            [[args.fx, 0, args.cx], [0, args.fy, args.cy], [0, 0, 1]],
            dtype=float,
        )

    system = VisualOdometrySystem(
        feature_extractor=FeatureExtractor(camera_matrix=camera_matrix)
    )
    positions = system.process(args.video)
    print(f"Processed trajectory positions: {len(positions)}")
    system.plot_trajectory(positions)


if __name__ == "__main__":
    main()
