import unittest
import numpy as np

from src.map_software.robot import Robot


class RobotTests(unittest.TestCase):
    def test_pose_accumulation(self):
        robot = Robot()
        transform = np.eye(4)
        transform[0, 3] = 2.0

        pose = robot.update_pose(transform)

        self.assertEqual(pose[0, 3], 2.0)
        self.assertEqual(pose[1, 3], 0.0)
        self.assertEqual(pose[2, 3], 0.0)


if __name__ == "__main__":
    unittest.main()
