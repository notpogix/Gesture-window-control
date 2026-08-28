\# Gesture Cursor 🖐️



Control your mouse cursor and drag windows around your screen using nothing but your webcam and hand gestures — no extra hardware required.



!\[Python](https://img.shields.io/badge/python-3.11-blue)

!\[License](https://img.shields.io/badge/license-MIT-green)

!\[Platform](https://img.shields.io/badge/platform-Windows-lightgrey)



\## Features



\- 🖱️ \*\*Cursor control\*\* — move your index finger, the system cursor follows

\- 🤏 \*\*Pinch to grab\*\* — pinch thumb + index finger together to grab any window under your cursor

\- 🪟 \*\*Window dragging\*\* — move your hand while pinching to drag the window; relax your hand to release

\- 🎥 \*\*Live camera overlay\*\* — see your hand landmarks and current gesture state in real time

\- ⚙️ \*\*Fully configurable\*\* — tune sensitivity, smoothing, and detection thresholds in one file

\- 💻 \*\*100% local \& free\*\* — no cloud APIs, no paid services, no internet required after setup



\## Demo



\*(Add a GIF or screenshot here once you've tested it — this is the single biggest thing that makes a GitHub repo look professional.)\*



\## Requirements



\- Windows 10/11

\- Python 3.10–3.12

\- A webcam



\## Installation



```bash

git clone https://github.com/YOUR\_USERNAME/gesture-cursor.git

cd gesture-cursor

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



\## Usage



```bash

python main.py

```



\- Move your \*\*index finger\*\* to move the cursor

\- \*\*Pinch\*\* your thumb and index finger together over any window to grab it

\- Move your hand while pinching to drag the window

\- Release the pinch to drop the window

\- Press \*\*`q`\*\* in the camera window to quit



\## Configuration



All tunable parameters live in `config.py`:



| Setting | Description |

|---|---|

| `SMOOTHING` | Higher = smoother but laggier cursor movement |

| `PINCH\_THRESHOLD` | How close fingers must be to trigger a pinch |

| `FRAME\_MARGIN` | Shrinks the usable camera area so you don't need to reach frame edges |

| `SHOW\_CAMERA\_WINDOW` | Toggle the debug camera preview |



\## How it works



1\. \*\*\[MediaPipe Hands](https://developers.google.com/mediapipe)\*\* detects 21 hand landmarks per frame from the webcam feed

2\. The index fingertip position is mapped from camera space to screen space and sent to the OS cursor via \*\*PyAutoGUI\*\*

3\. Thumb–index distance is monitored as a simple pinch state machine

4\. On pinch, \*\*PyWin32\*\* finds the real OS window under the cursor and its position is updated every frame while the pinch is held



\## Tech stack



\- \[OpenCV](https://opencv.org/) — webcam capture

\- \[MediaPipe](https://developers.google.com/mediapipe) — hand landmark detection

\- \[PyAutoGUI](https://pyautogui.readthedocs.io/) — cursor control

\- \[PyGetWindow](https://github.com/asweigart/PyGetWindow) + \[PyWin32](https://github.com/mhammond/pywin32) — window management



\## Known limitations



\- Single-hand tracking only (by design, for stability)

\- Windows only (Win32 API dependency)

\- Requires reasonable, consistent lighting for reliable tracking



\## License



MIT — see \[LICENSE](LICENSE)

