

from typing import Optional, Tuple
import math
import cv2
import mediapipe as mp

EyePos = Tuple[float, float, float]


class FaceTracker:
    """Wraps MediaPipe FaceMesh and a CV2 video capture.

    get_eye_position() -> Optional[(x, y, z)] returns normalized x/y in
    [0,1] with a heuristic z (inverse of iris distance). The X value is
    mirrored (1.0 - x) so the result behaves like a mirror for the user.
    """

    def __init__(self, camera_id: int = 0, width: int = 640, height: int = 480):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.cap = cv2.VideoCapture(camera_id)
        # Lower resolution for performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.calibrated = False
        self.base_x = 0.5
        self.base_y = 0.5
        self.base_depth_scale = 1.0

    def get_eye_position(self) -> Optional[EyePos]:
        success, image = self.cap.read()
        if not success:
            return None

        # Mark image as read-only for MediaPipe performance
        image.flags.writeable = False
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)
        image.flags.writeable = True

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            left_iris = landmarks[468]
            right_iris = landmarks[473]

            avg_x = (left_iris.x + right_iris.x) / 2.0
            avg_y = (left_iris.y + right_iris.y) / 2.0

            eye_distance = math.hypot(left_iris.x - right_iris.x, left_iris.y - right_iris.y)
            if eye_distance < 0.001:
                eye_distance = 0.001
            estimated_z = 1.0 / eye_distance

            # Mirror X so UI behaves like a mirror
            return (1.0 - avg_x, avg_y, estimated_z)

        return None

    def calibrate(self, current_pos: Optional[EyePos]) -> None:
        if current_pos:
            self.base_x, self.base_y, self.base_depth_scale = current_pos
            self.calibrated = True
            print("Calibration Complete!")

    def cleanup(self) -> None:
        try:
            if self.cap and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass


__all__ = ["FaceTracker"]
