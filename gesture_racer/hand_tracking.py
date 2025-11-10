from dataclasses import dataclass
from typing import List, Optional
import cv2
import mediapipe as mp


@dataclass
class HandData:
    x: int
    y: int
    label: str  # 'Left', 'Right', or 'Unknown'
    landmarks: Optional[object] = None


class HandTracker:
    def __init__(
        self,
        model_complexity: int = 0,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.6,
    ):
        self.model_complexity = model_complexity
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands_ctx = None

    def __enter__(self):
        self.hands_ctx = self.mp_hands.Hands(
            model_complexity=self.model_complexity,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.hands_ctx:
            self.hands_ctx.close()
            self.hands_ctx = None

    def process(self, bgr_frame) -> List[HandData]:
        if self.hands_ctx is None:
            raise RuntimeError("HandTracker must be used as a context manager or call __enter__ first.")

        h, w, _ = bgr_frame.shape
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        results = self.hands_ctx.process(rgb_frame)

        hands: List[HandData] = []
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Wrist landmark in pixel coordinates
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                x_px, y_px = int(wrist.x * w), int(wrist.y * h)

                # Handedness
                if results.multi_handedness and idx < len(results.multi_handedness):
                    label = results.multi_handedness[idx].classification[0].label
                else:
                    label = "Unknown"

                hands.append(HandData(x=x_px, y=y_px, label=label, landmarks=hand_landmarks))

        return hands