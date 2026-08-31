"""
Tracks fist state (open hand vs. closed fist) as a simple state machine:
IDLE -> GRABBING -> IDLE. Uses a frame-confirmation buffer so a single
noisy frame during fast hand motion can't falsely trigger a release.
"""

import config


class GestureState:
    def __init__(self):
        self.is_fist = False
        self._pending_state = None
        self._pending_count = 0

    def update(self, curled_finger_count: int):
        """
        Returns one of: "fist_start", "fist_hold", "fist_end", "idle"
        """
        raw_fist = curled_finger_count >= config.FIST_FINGER_COUNT

        if raw_fist == self.is_fist:
            self._pending_state = None
            self._pending_count = 0
            return "fist_hold" if self.is_fist else "idle"

        if self._pending_state == raw_fist:
            self._pending_count += 1
        else:
            self._pending_state = raw_fist
            self._pending_count = 1

        if self._pending_count >= config.CONFIRM_FRAMES:
            self.is_fist = raw_fist
            self._pending_state = None
            self._pending_count = 0
            return "fist_start" if self.is_fist else "fist_end"

        return "fist_hold" if self.is_fist else "idle"