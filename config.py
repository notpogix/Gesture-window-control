"""
Configuration settings for Gesture Cursor.
Tune these values to adjust sensitivity and behavior.
"""

# --- Camera settings ---
CAMERA_INDEX = 0
FRAME_WIDTH = 424
FRAME_HEIGHT = 240

# --- Hand tracking ---
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6
MODEL_COMPLEXITY = 0

# --- Cursor mapping ---
FRAME_MARGIN = 60
SMOOTHING = 0.35

# --- Pinch / gesture detection (window dragging) ---
PINCH_THRESHOLD = 0.05

# --- Click gestures ---
# A finger counts as "bent" when its tip is this much closer to the wrist
# than its PIP joint (normalized 0-1 distance). Higher = requires a more
# obvious bend.
BEND_THRESHOLD = 0.04

# Max time (seconds) between two left-click bends to count as a double click.
DOUBLE_CLICK_WINDOW = 0.35

# Minimum time (seconds) a finger must stay straight before it can trigger
# another click — prevents accidental rapid-fire clicking.
CLICK_COOLDOWN = 0.25

# --- UI ---
SHOW_CAMERA_WINDOW = False
SHOW_OVERLAY = True          # can also be toggled live with the 'o' hotkey (see README)