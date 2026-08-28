"""
Gesture Cursor — control your mouse and drag windows using hand gestures
tracked through your webcam.

Run: python main.py
Quit: press Ctrl+C in the terminal.
"""

import cv2
import config
from src.hand_tracker import HandTracker
from src.cursor_controller import CursorController
from src.gesture_state import GestureState
from src.window_manager import WindowManager
from src.overlay import StatusOverlay


def main():
    cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("ERROR: Could not open webcam. Check CAMERA_INDEX in config.py.")
        return

    tracker = HandTracker()
    cursor = CursorController()
    gesture = GestureState()
    windows = WindowManager()
    overlay = StatusOverlay() if config.SHOW_OVERLAY else None

    print("Gesture Cursor running. Press Ctrl+C in this terminal to quit.")

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Failed to read from webcam.")
                break

            frame = cv2.flip(frame, 1)
            frame_h, frame_w = frame.shape[:2]

            hands_data = tracker.process(frame)

            if hands_data:
                hand_landmarks = hands_data[0]

                if config.SHOW_CAMERA_WINDOW:
                    tracker.draw_landmarks(frame, hand_landmarks)

                index_norm = tracker.get_landmark_normalized(
                    hand_landmarks, tracker.INDEX_FINGER_TIP
                )
                thumb_norm = tracker.get_landmark_normalized(
                    hand_landmarks, tracker.THUMB_TIP
                )

                screen_x, screen_y = cursor.map_to_screen(
                    index_norm[0], index_norm[1], frame_w, frame_h
                )
                final_x, final_y = cursor.move_to(screen_x, screen_y)

                event = gesture.update(thumb_norm, index_norm)
                if event == "pinch_start":
                    windows.try_grab(final_x, final_y)
                elif event == "pinch_hold":
                    windows.drag(final_x, final_y)
                elif event == "pinch_end":
                    windows.release()

                if overlay:
                    overlay.set_status("dragging" if windows.is_dragging else "tracking")
            else:
                windows.release()
                if overlay:
                    overlay.set_status("idle")

            if config.SHOW_CAMERA_WINDOW:
                cv2.imshow("Gesture Cursor - press q to quit", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            if overlay:
                overlay.pump()

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if overlay:
            overlay.close()


if __name__ == "__main__":
    main()