"""
Maps hand position to system cursor position, with smoothing and a
small dead-zone to eliminate micro-jitter from landmark noise.
"""

import pyautogui
import config

pyautogui.FAILSAFE = False
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0  # remove PyAutoGUI's default 0.1s delay after every call


class CursorController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = self.screen_w // 2, self.screen_h // 2

    def map_to_screen(self, norm_x, norm_y, frame_w, frame_h):
        px = norm_x * frame_w
        py = norm_y * frame_h

        margin = config.FRAME_MARGIN
        usable_w = max(frame_w - 2 * margin, 1)
        usable_h = max(frame_h - 2 * margin, 1)

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

        # Dead zone: skip the OS call entirely for sub-threshold movement
        if abs(final_x - self.prev_x) < config.DEAD_ZONE_PX and \
           abs(final_y - self.prev_y) < config.DEAD_ZONE_PX:
            return self.prev_x, self.prev_y

        pyautogui.moveTo(final_x, final_y, _pause=False)
        self.prev_x, self.prev_y = final_x, final_y
        return final_x, final_y