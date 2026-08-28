"""
Maps hand position to system cursor position, with smoothing.
"""

import pyautogui
import config

pyautogui.FAILSAFE = False  # prevent PyAutoGUI's corner-abort during fast hand motion


class CursorController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = self.screen_w // 2, self.screen_h // 2

    def map_to_screen(self, norm_x, norm_y, frame_w, frame_h):
        """
        Convert normalized hand landmark (0-1) to screen pixel coordinates,
        applying the frame margin so full screen reach doesn't require
        reaching the camera frame edges.
        """
        px = norm_x * frame_w
        py = norm_y * frame_h

        margin = config.FRAME_MARGIN
        usable_w = frame_w - 2 * margin
        usable_h = frame_h - 2 * margin
        usable_w = max(usable_w, 1)
        usable_h = max(usable_h, 1)

        rel_x = (px - margin) / usable_w
        rel_y = (py - margin) / usable_h
        rel_x = min(max(rel_x, 0), 1)
        rel_y = min(max(rel_y, 0), 1)

        screen_x = rel_x * self.screen_w
        screen_y = rel_y * self.screen_h
        return screen_x, screen_y

    def move_to(self, screen_x, screen_y):
        smooth = config.SMOOTHING
        final_x = self.prev_x + (screen_x - self.prev_x) * (1 - smooth)
        final_y = self.prev_y + (screen_y - self.prev_y) * (1 - smooth)

        pyautogui.moveTo(final_x, final_y)
        self.prev_x, self.prev_y = final_x, final_y
        return final_x, final_y