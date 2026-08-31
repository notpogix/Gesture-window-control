"""
Gesture Cursor — control your mouse and drag windows using hand gestures
tracked through your webcam.

Open hand + index finger -> move cursor
Make a fist over a window -> grab and drag it
Open hand again -> release

Run: python main.py
Quit: press Ctrl+C in the terminal.
"""

import cv2
import time
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
    cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("ERROR: Could not open webcam. Check CAMERA_INDEX in config.py.")
        return

    tracker = HandTracker()
    cursor = CursorController()
    gesture = GestureState()
    windows = WindowManager()
    overlay = StatusOverlay() if config.SHOW_OVERLAY else None

    frame_budget = 1.0 / config.TARGET_FPS

    print("Gesture Cursor running. Press Ctrl+C in this terminal to quit.")

    try:
        while True:
            loop_start = time.perf_counter()

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

                curled_count = tracker.count_curled_fingers(hand_landmarks)
                event = gesture.update(curled_count)

                track_x, track_y = tracker.get_landmark_normalized(
                    hand_landmarks, tracker.INDEX_FINGER_MCP
                )

                screen_x, screen_y = cursor.map_to_screen(
                    track_x, track_y, frame_w, frame_h
                )
                final_x, final_y = cursor.move_to(screen_x, screen_y)

                if event == "fist_start":
                    windows.try_grab(final_x, final_y)
                elif event == "fist_hold":
                    windows.drag(final_x, final_y)
                elif event == "fist_end":
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

            # Frame pacing: sleep off any leftover time in the budget so the
            # loop runs at a stable, consistent rate instead of racing ahead
            elapsed = time.perf_counter() - loop_start
            sleep_time = frame_budget - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if overlay:
            overlay.close()


if __name__ == "__main__":
    main()