"""User-facing input for the prototype."""


class User:
    """Collects the user's identity and selected video source."""

    def __init__(self, user_id=None, video_path=None):
        self.id = user_id
        self.video_path = video_path

    def request_data_source(self):
        """Collect the video source from the command line."""
        if self.id is None:
            self.id = input("ID: ").strip()
        if self.video_path is None:
            self.video_path = input("Video path: ").strip()
        if not self.video_path:
            raise ValueError("A video path is required.")
        return self.id, self.video_path
