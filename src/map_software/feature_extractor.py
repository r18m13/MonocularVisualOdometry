"""Visual feature matching and relative-pose estimation."""

import cv2
import numpy as np


class FeatureExtractor:
    """Estimate relative camera motion from two monocular frames.

    The translation returned by a monocular essential-matrix decomposition
    has an unknown absolute scale.
    """

    def __init__(self, camera_matrix=None, nfeatures=3000):
        self.nfeatures = nfeatures
        self.camera_matrix = (
            np.asarray(camera_matrix, dtype=np.float64)
            if camera_matrix is not None
            else None
        )

    def _camera_matrix(self, frame):
        if self.camera_matrix is not None:
            return self.camera_matrix

        height, width = frame.shape[:2]
        # Demonstration defaults only; real calibration should be supplied.
        focal = float(max(width, height))
        return np.array(
            [[focal, 0.0, width / 2.0],
             [0.0, focal, height / 2.0],
             [0.0, 0.0, 1.0]],
            dtype=np.float64,
        )

    def extract_features(self, frame_0, frame_1):
        """Return (R, t) for two frames or raise ValueError if estimation fails."""
        if frame_0 is None or frame_1 is None:
            raise ValueError("Both frames are required.")

        orb = cv2.ORB_create(nfeatures=self.nfeatures)
        keypoints0, descriptors0 = orb.detectAndCompute(frame_0, None)
        keypoints1, descriptors1 = orb.detectAndCompute(frame_1, None)

        if descriptors0 is None or descriptors1 is None:
            raise ValueError("Could not extract descriptors from both frames.")

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = sorted(
            matcher.match(descriptors0, descriptors1),
            key=lambda match: match.distance,
        )

        if len(matches) < 8:
            raise ValueError("At least 8 feature matches are required.")

        points0 = np.float32([keypoints0[m.queryIdx].pt for m in matches])
        points1 = np.float32([keypoints1[m.trainIdx].pt for m in matches])
        K = self._camera_matrix(frame_0)

        E, mask = cv2.findEssentialMat(
            points0,
            points1,
            K,
            method=cv2.RANSAC,
            prob=0.999,
            threshold=1.0,
        )
        if E is None:
            raise ValueError("Essential matrix estimation failed.")

        _, R, t, pose_mask = cv2.recoverPose(E, points0, points1, K)
        if R is None or t is None:
            raise ValueError("Relative pose recovery failed.")

        return R, t.reshape(3)
