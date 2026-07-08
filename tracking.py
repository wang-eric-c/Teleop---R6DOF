
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import config


class HandTracker:
    def __init__(self):
        base = python.BaseOptions(model_asset_path=config.MODEL_PATH)
        opts = vision.HandLandmarkerOptions(
            base_options=base,
            num_hands=config.NUM_HANDS,
            min_hand_detection_confidence=config.DETECT_CONF,
            min_tracking_confidence=config.TRACK_CONF,
        )
        self._landmarker = vision.HandLandmarker.create_from_options(opts)

    def detect(self, frame_bgr):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._landmarker.detect(mp_image)
        if not result.hand_landmarks:
            return None
        return result.hand_landmarks[0]

    @staticmethod
    def draw(frame_bgr, landmarks):
        if landmarks is None:
            return
        h, w = frame_bgr.shape[:2]
        for p in landmarks:
            cv2.circle(frame_bgr, (int(p.x * w), int(p.y * h)), 4, (0, 255, 0), -1)