"""
Finds and drags real OS windows on Windows, using pygetwindow + pywin32.
Once a window is grabbed, it stays locked to that window until an explicit
release. Grabbed windows are brought to the front. Redundant sub-pixel
moves are skipped to reduce OS call overhead and keep dragging smooth.
"""

import pygetwindow as gw
import win32gui
import config


class WindowManager:
    def __init__(self):
        self.grabbed_window = None
        self.grab_offset_x = 0
        self.grab_offset_y = 0
        self._last_left = None
        self._last_top = None

    @staticmethod
    def _window_under_point(x, y):
        hwnd = win32gui.WindowFromPoint((int(x), int(y)))
        if hwnd == 0:
            return None
        root = win32gui.GetAncestor(hwnd, 2)  # GA_ROOT = 2
        return root if root else hwnd

    @staticmethod
    def _bring_to_front(hwnd):
        try:
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

    def try_grab(self, screen_x, screen_y):
        if self.grabbed_window is not None:
            return True

        hwnd = self._window_under_point(screen_x, screen_y)
        if not hwnd:
            return False

        title = win32gui.GetWindowText(hwnd)
        if not title:
            return False

        try:
            win = gw.Win32Window(hwnd)
        except Exception:
            return False

        self.grabbed_window = win
        self.grab_offset_x = screen_x - win.left
        self.grab_offset_y = screen_y - win.top
        self._last_left = win.left
        self._last_top = win.top

        self._bring_to_front(hwnd)
        return True

    def drag(self, screen_x, screen_y):
        if self.grabbed_window is None:
            return
        try:
            new_left = int(screen_x - self.grab_offset_x)
            new_top = int(screen_y - self.grab_offset_y)

            if self._last_left is not None:
                delta = abs(new_left - self._last_left) + abs(new_top - self._last_top)
                if delta < config.MIN_DRAG_DELTA_PX:
                    return  # skip negligible move, saves an OS call every frame

            self.grabbed_window.moveTo(new_left, new_top)
            self._last_left, self._last_top = new_left, new_top
        except Exception:
            self.grabbed_window = None

    def release(self):
        self.grabbed_window = None
        self._last_left = None
        self._last_top = None

    @property
    def is_dragging(self):
        return self.grabbed_window is not None