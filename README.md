🎮 Gesture Driver

Professional, modular hand‑gesture steering for games and experiences — powered by MediaPipe and OpenCV. Control forward, braking, reversing, and steering using your hands, with a futuristic multi‑theme HUD and smooth tilt‑based wheel visualization.

🚗 Features

🖐️ Real-time hand tracking using MediaPipe

🎮 Keyboard control simulation for W, A, S, D

🧭 Two modes (modular design):

- Modular App (recommended): main.py → Clean UI, themed overlay, continuous tilt‑based steering
- Legacy scripts: steering.py (pynput), key_input.py (Windows ctypes)

🪟 Works with Windows key events or via pynput keyboard

📷 Clean, themed UI overlay using OpenCV (Neo Green, Ocean Blue, Sunset Orange, Cyber Purple, HOLO FLUX, Dark themes)

⚙️ Tech Used

Python 3.x

OpenCV – camera input and visualization

MediaPipe – hand landmark detection

ctypes / pynput – virtual keyboard input

📦 Modular Architecture

- gesture_racer/config.py — central configuration
- gesture_racer/camera.py — camera abstraction
- gesture_racer/hand_tracking.py — MediaPipe wrapper
- gesture_racer/gestures.py — pure gesture decision logic
- gesture_racer/input_controller.py — cross‑platform key input
- gesture_racer/ui/theme.py — swappable color themes
- gesture_racer/ui/overlay.py — advanced HUD rendering

🧪 Build a Windows .exe with PyInstaller

PyInstaller builds are OS-specific. To create a Windows .exe, run the build on a Windows machine:

1) Install Python 3.11 for Windows, then open Command Prompt in the project folder.
2) Run the build script:

   scripts\build_windows_pyinstaller.bat

This will:
- Create a virtual environment
- Install dependencies and PyInstaller
- Build using build\pyinstaller_win.spec

Output: dist\GestureRacer.exe

If you prefer a direct command instead of the spec:

   pyinstaller --onefile --name GestureRacer --collect-all mediapipe --collect-all cv2 --collect-all jaxlib --collect-all jax --collect-all numpy main.py

Note: The onefile exe can be large due to MediaPipe and its native libraries. Using the spec file ensures required data and submodules are bundled.

📷 Custom App Icon

- Save your icon PNG (like the one you shared) to assets/icon.png.
- The build script converts it into assets/app.ico automatically using Pillow and embeds it into the exe.
- Recommended: square 256x256 PNG with transparent background.

Quick Start (macOS/Linux)
1) Create a Python 3.11 virtual environment and install dependencies:
   python3.11 -m venv .venv311
   .venv311/bin/python -m pip install -r requirements.txt
2) Run the app:
   .venv311/bin/python main.py
3) Give permissions if prompted (macOS): Accessibility, Input Monitoring, Camera.

Quick Start (Windows)
- Install Python 3.11, then:
  py -3.11 -m venv .venv311
  .venv311\Scripts\python -m pip install -r requirements.txt
  .venv311\Scripts\python main.py
- Legacy script options:
  - steering.py (pynput)
  - key_input.py (Windows ctypes)

🛠️ Troubleshooting on Windows

- Webcam permissions: Windows will prompt the first time the app accesses the camera.
- Keyboard injection: For games to receive key events, ensure the game window is focused. Some anti-cheat systems may block simulated input.
- Antivirus flags: Large onefile executables may be scanned. Add an exclusion if needed.
- If packing fails, try: pyinstaller --clean --noconfirm build\pyinstaller_win.spec

🚀 Run (recommended)

1) Create and use Python 3.11 virtual environment

   python3.11 -m venv .venv311
   .venv311/bin/python -m pip install -r requirements.txt

2) Start the app

   .venv311/bin/python main.py

3) macOS permissions (to send key presses):

   - System Settings → Privacy & Security → Accessibility → enable Terminal/Python
   - System Settings → Privacy & Security → Input Monitoring → enable if prompted
   - System Settings → Privacy & Security → Camera → enable Terminal/Python

Controls
- q: quit
- t: cycle all themes
- d: cycle dark themes
- - / = or +: decrease/increase steering sensitivity (gain)
- [ / ]: widen/narrow deadband around center
- h: toggle debug chips
- r: reset tuning

Configuration (gesture_racer/config.py)
- camera_index, frame_flip
- detection/tracking confidence
- brake_distance_px, turn_tilt_threshold
- steering_gain, max_steering_deg, turn_deadband_deg
- smoothing_alpha_angle
- ui_intensity, particle_max, trail_length, grid_alpha, scanlines_alpha, hex_alpha
- background_blur_enabled, background_blur_ksize, background_blur_sigma
- handle_enabled, grip_threshold_px, handle_radius_px, handle_max_length_px
- theme_name: neo_green | ocean_blue | sunset_orange | cyber_purple | holo_flux | dark_stealth | dark_crimson | dark_cyan

Themes & UI
- Multi‑color neon palettes and dark modes
- Wheel with rotating tick ring, pulsing holographic ring
- Hex grid with parallax, scanlines, segment bar
- Wrist handles that respond to pinch and tilt

Project Structure (top‑level)
- gesture_racer/ … modular package
- main.py … modern app entry
- steering.py, key_input.py … legacy demos
- assets/ … icon and version metadata
- scripts/ … build helpers
- build/ … PyInstaller spec
- README.md, LICENSE, requirements.txt

Troubleshooting
- Ensure the target game window is focused to receive inputs
- macOS: grant Accessibility, Input Monitoring, Camera
- Large onefile exe sizes are normal due to native libs

License
- MIT License. See LICENSE for details.
