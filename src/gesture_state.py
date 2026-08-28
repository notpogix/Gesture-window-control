"""
Tracks pinch state (thumb tip <-> index tip distance) as a simple
state machine: IDLE -> PINCHING -> IDLE. Release is instant — the moment
the distance crosses back over the threshold.
"""

import math
import config


class GestureState:
    def __init__(self):
        self.is_pinching = False

    @staticmethod
    def _distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def update(self, thumb_norm, index_norm):
        """
        Returns one of: "pinch_start", "pinch_hold", "pinch_end", "idle"
        """
        dist = self._distance(thumb_norm, index_norm)

        if dist < config.PINCH_THRESHOLD:
            if not self.is_pinching:
                self.is_pinching = True
                return "pinch_start"
            return "pinch_hold"
        else:
            if self.is_pinching:
                self.is_pinching = False
                return "pinch_end"
            return "idle"