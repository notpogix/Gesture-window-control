"""
Configuration settings for Gesture Cursor.
Tune these values to adjust sensitivity and behavior.
"""

# --- Camera settings ---
CAMERA_INDEX = 0
FRAME_WIDTH = 424
FRAME_HEIGHT = 240
TARGET_FPS = 60

# --- Hand tracking ---
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6
MODEL_COMPLEXITY = 0

# --- Cursor mapping ---
FRAME_MARGIN = 60
SMOOTHING = 0.6              # higher = smoother, slightly more lag
DEAD_ZONE_PX = 2             # ignore cursor moves smaller than this (kills micro-jitter)

# --- Fist / gesture detection (window dragging) ---
BEND_THRESHOLD = 0.04
FIST_FINGER_COUNT = 4
CONFIRM_FRAMES = 3

# --- Window drag optimization ---
MIN_DRAG_DELTA_PX = 2        # skip redundant window moves smaller than this

# --- UI ---
SHOW_CAMERA_WINDOW = False
SHOW_OVERLAY = True