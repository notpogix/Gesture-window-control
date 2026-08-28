"""
Finds and drags real OS windows on Windows, using pygetwindow + pywin32.
Once a window is grabbed, it stays locked to that window until an explicit
release — fast cursor movement during a drag will never switch targets.
"""

import pygetwindow as gw
import win32gui


class WindowManager:
    def __init__(self):
        self.grabbed_window = None
        self.grab_offset_x = 0
        self.grab_offset_y = 0

    @staticmethod
    def _window_under_point(x, y):
        hwnd = win32gui.WindowFromPoint((int(x), int(y)))
        if hwnd == 0:
            return None
        root = win32gui.GetAncestor(hwnd, 2)  # GA_ROOT = 2
        return root if root else hwnd

    def try_grab(self, screen_x, screen_y):
        """Call ONLY on pinch_start. Ignored if already dragging something."""
        if self.grabbed_window is not None:
            return True  # already locked onto a window, don't re-grab

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
        return True

    def drag(self, screen_x, screen_y):
        """Call on pinch_hold. Only moves the already-locked window."""
        if self.grabbed_window is None:
            return
        try:
            new_left = int(screen_x - self.grab_offset_x)
            new_top = int(screen_y - self.grab_offset_y)
            self.grabbed_window.moveTo(new_left, new_top)
        except Exception:
            self.grabbed_window = None

    def release(self):
        """Call on pinch_end (or when hand is lost)."""
        self.grabbed_window = None

    @property
    def is_dragging(self):
        return self.grabbed_window is not None