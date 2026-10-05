"""Video input abstraction."""


class Sensor:
    """Represents the source of visual data used by the prototype."""

    def __init__(self, sensor_type="monocular_camera", data=None):
        self.type = sensor_type
        self.data = data

    def acquire_data(self, path=None):
        """Set and return the video data source."""
        self.data = path if path is not None else input("Video path: ").strip()
        if not self.data:
            raise ValueError("A video path is required.")
        return self.data
