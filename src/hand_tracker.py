"""
Wraps MediaPipe Hands to give simple, clean landmark data per frame.
"""

import cv2
import mediapipe as mp
import config


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
            model_complexity=config.MODEL_COMPLEXITY,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def process(self, frame_bgr):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        self.results = self.hands.process(frame_rgb)

        hands_data = []
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                hands_data.append(hand_landmarks)
        return hands_data

    def draw_landmarks(self, frame_bgr, hand_landmarks):
        self.mp_draw.draw_landmarks(
            frame_bgr, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
        )

    @staticmethod
    def get_landmark_xy(hand_landmarks, index, frame_width, frame_height):
        lm = hand_landmarks.landmark[index]
        return int(lm.x * frame_width), int(lm.y * frame_height)

    @staticmethod
    def get_landmark_normalized(hand_landmarks, index):
        lm = hand_landmarks.landmark[index]
        return lm.x, lm.y

    def is_finger_bent(self, hand_landmarks, tip_idx, pip_idx):
        """
        A finger is 'bent' when its tip is closer to the wrist than its
        PIP joint is — i.e. curled inward, independent of hand rotation.
        """
        wrist = self.get_landmark_normalized(hand_landmarks, self.WRIST)
        tip = self.get_landmark_normalized(hand_landmarks, tip_idx)
        pip = self.get_landmark_normalized(hand_landmarks, pip_idx)

        def dist(a, b):
            return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

        tip_to_wrist = dist(tip, wrist)
        pip_to_wrist = dist(pip, wrist)

        return (pip_to_wrist - tip_to_wrist) > config.BEND_THRESHOLD

    # Landmark indices (MediaPipe hand model)
    WRIST = 0
    THUMB_TIP = 4
    INDEX_FINGER_TIP = 8
    INDEX_FINGER_PIP = 6
    MIDDLE_FINGER_TIP = 12
    MIDDLE_FINGER_PIP = 10