"""
Tracks pinch state (thumb tip <-> index tip distance) as a simple
state machine: IDLE -> PINCHING -> IDLE.

Uses a small frame-confirmation buffer so a single noisy frame during
fast hand motion can't falsely trigger a release mid-drag.
"""

import math
import config


class GestureState:
    def __init__(self):
        self.is_pinching = False
        self._pending_state = None
        self._pending_count = 0
        self.CONFIRM_FRAMES = 2  # frames a state must hold before it's accepted

    @staticmethod
    def _distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def update(self, thumb_norm, index_norm):
        """
        Returns one of: "pinch_start", "pinch_hold", "pinch_end", "idle"
        """
        dist = self._distance(thumb_norm, index_norm)
        raw_pinching = dist < config.PINCH_THRESHOLD

        if raw_pinching == self.is_pinching:
            # Already in this state — no confirmation needed, reset buffer
            self._pending_state = None
            self._pending_count = 0
            return "pinch_hold" if self.is_pinching else "idle"

        # Raw reading disagrees with current state — require confirmation
        if self._pending_state == raw_pinching:
            self._pending_count += 1
        else:
            self._pending_state = raw_pinching
            self._pending_count = 1

        if self._pending_count >= self.CONFIRM_FRAMES:
            self.is_pinching = raw_pinching
            self._pending_state = None
            self._pending_count = 0
            return "pinch_start" if self.is_pinching else "pinch_end"

        # Not yet confirmed — keep reporting the current stable state
        return "pinch_hold" if self.is_pinching else "idle"