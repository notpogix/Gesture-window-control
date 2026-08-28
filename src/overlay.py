"""
Small always-on-top overlay in the bottom-right corner showing gesture
status. Uses Windows color-key transparency (-transparentcolor) so the
background is genuinely see-through, not translucent black.
"""

import tkinter as tk


class StatusOverlay:
    COLORS = {
        "tracking": "#2ecc71",
        "dragging": "#f1c40f",
        "idle": "#7f8c8d",
        "click": "#3498db",
    }

    TRANSPARENT_KEY = "#010101"  # near-black, unlikely to appear elsewhere

    def __init__(self, width=170, height=40, margin=20):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # Color-key transparency: this exact color becomes a see-through hole
        self.root.config(bg=self.TRANSPARENT_KEY)
        self.root.attributes("-transparentcolor", self.TRANSPARENT_KEY)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w - width - margin
        y = screen_h - height - margin - 50
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # A small solid pill behind the text so it's readable without a
        # full box — drawn with rounded look via a Canvas oval/rect.
        self.canvas = tk.Canvas(
            self.root, width=width, height=height,
            bg=self.TRANSPARENT_KEY, highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.pill = self.canvas.create_rectangle(
            2, 2, width - 2, height - 2,
            fill="#1c1c1c", outline="",
        )
        self.text_id = self.canvas.create_text(
            width // 2, height // 2,
            text="TRACKING", fill="white",
            font=("Segoe UI", 11, "bold"),
        )

        self.visible = True

    def set_status(self, status: str):
        color = self.COLORS.get(status, "#7f8c8d")
        self.canvas.itemconfig(self.text_id, text=status.upper(), fill=color)

    def toggle(self):
        if self.visible:
            self.root.withdraw()
        else:
            self.root.deiconify()
        self.visible = not self.visible

    def pump(self):
        self.root.update_idletasks()
        self.root.update()

    def close(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass