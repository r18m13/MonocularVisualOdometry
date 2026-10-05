import unittest
import numpy as np
from src.map_software.visual_odometry import VisualOdometrySystem


class InverseTransformTests(unittest.TestCase):
    def test_inverse_undoes_transform(self):
        theta = np.deg2rad(30)
        R = np.array([[np.cos(theta), -np.sin(theta), 0],
                      [np.sin(theta),  np.cos(theta), 0],
                      [0, 0, 1]])
        t = np.array([1.0, 2.0, 3.0])

        forward = VisualOdometrySystem._homogeneous_transform(R, t)
        inverse = VisualOdometrySystem._inverse_transform(R, t)

        np.testing.assert_allclose(forward @ inverse, np.eye(4), atol=1e-9)


if __name__ == "__main__":
    unittest.main()