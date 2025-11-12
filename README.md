# Gesture Driver

<br>
<p align="center">
  <img src="assets/icon.png" alt="Gesture Driver Logo" height="92"/>
</p>

<p align="center">
  <b>Professional, modular hand‑gesture steering for games and interactive experiences.</b><br>
  🚗 Powered by <a href="https://mediapipe.dev/">MediaPipe</a> & <a href="https://opencv.org/">OpenCV</a>. Control forward, braking, reversing, and steering using your hands—with a futuristic multi‑theme HUD and real‑time visualization.
</p>
<br>

<p align="center">
  <a href="https://github.com/Daivik1520/gesture-driver/actions/workflows/build.yml"><img src="https://img.shields.io/github/actions/workflow/status/Daivik1520/gesture-driver/build.yml?branch=main&label=build&logo=github" alt="Build Status"></a>
  <a href="https://github.com/Daivik1520/gesture-driver/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Daivik1520/gesture-driver?logo=open-source-initiative" alt="License"></a>
  <a href="https://github.com/Daivik1520/gesture-driver"><img src="https://img.shields.io/github/stars/Daivik1520/gesture-driver?logo=github" alt="Stars"></a>
  <a href="https://github.com/Daivik1520/gesture-driver/issues"><img src="https://img.shields.io/github/issues/Daivik1520/gesture-driver?logo=github" alt="Open Issues"></a>
  <img src="https://img.shields.io/badge/python-3.11-blue.svg?logo=python" alt="Python 3.11">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-success?logo=windows" alt="Platform">
</p>

---

## 📑 Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Windows](#windows)
  - [macOS / Linux](#macos--linux)
- [Usage](#usage)
- [Build for Windows (.exe)](#build-for-windows-exe)
- [Customization](#customization)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## 🚗 Features

- **🖐️ Real-time Hand Tracking:** Powered by [MediaPipe](https://mediapipe.dev/)
- **🎮 Keyboard Control Simulation:** Virtual W, A, S, D controls for driving games
- **🧭 Modular Modes:**
  - **App Mode:** Continuous tilt‑based steering; modern themed UI overlay
  - **Legacy Scripts:** For classic steering methods (pynput/ctypes)
- **📷 Themed Overlays:** Futuristic HUD, switchable neon & dark color themes
- **🪟 Works Cross-Platform:** Simulates Windows key events or uses `pynput`
- **⚙️ Tech Stack:** Python 3.11, OpenCV, MediaPipe, ctypes, pynput, modular codebase

---

## ⚡️ Quick Start

### Windows


🔒 Grant permissions if prompted (Accessibility, Input Monitoring, Camera).

---

## ▶️ Usage

- **Controls:**
  - `q`: Quit app
  - `t`: Cycle themes
  - `d`: Cycle dark themes
  - `- / =`: Adjust steering sensitivity
  - `[ / ]`: Adjust steering deadband
  - `h`: Toggle debug chips
  - `r`: Reset tuning

- **Before You Start:**
  - Ensure the target game window is focused to receive simulated inputs.
  - On macOS, enable Python/Terminal in Accessibility, Input Monitoring, Camera.

---

## 🛠️ Build for Windows (.exe)

PyInstaller builds are OS-specific. To create a Windows executable:

1. Install Python 3.11 on Windows
2. Run from **Command Prompt** in the project directory:


#### _What it does:_
- Sets up a new venv
- Installs dependencies and PyInstaller
- Builds using `build/pyinstaller_win.spec`
- Output appears in `dist/GestureRacer.exe`

**One-liner PyInstaller alternative**:


> _Note: The executable may be large because of MediaPipe and native libraries. Using the provided `.spec` is safest._

#### Custom App Icon

- Put your 256x256 PNG (transparent) as `assets/icon.png`.
- The build script auto-generates & embeds an `assets/app.ico`.

---

## 🎨 Customization

**Themes:**  
Choose from Neo Green, Ocean Blue, Sunset Orange, Cyber Purple, HOLO FLUX, Dark Stealth, Dark Crimson, Dark Cyan.

The HUD supports:
- Neon palettes and deep dark modes
- Rotating “wheel” with tick ring
- Parallax grids, scanlines, holographic effects

---

## ⚙️ Configuration

Adjust `gesture_racer/config.py` for:
- Camera: `camera_index`, `frame_flip`
- ML: detection & tracking confidence
- Driving: `brake_distance_px`, `turn_tilt_threshold`
- Steering: `steering_gain`, `max_steering_deg`, `turn_deadband_deg`, `smoothing_alpha_angle`
- UI: `ui_intensity`, particles, trails, grids, hex, blur
- Handles: Pinch threshold, radius, max length
- Theme: `theme_name`

---


---

## 🛡️ Troubleshooting

- **Webcam**: Allow access the first time when prompted.
- **Keyboard Input**: Focus the game window.
- **Antivirus**: Large executables may be flagged. Add exclusions as needed.
- **Build Issues**: Try `pyinstaller --clean --noconfirm build\pyinstaller_win.spec`
- **macOS**: Grant permissions (Accessibility, Input Monitoring, Camera).

---

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.  
See [`LICENSE`](LICENSE) for details.

---

## 🤝 Contributing

Pull requests, bug reports, and feature suggestions are welcome!  
Open an [issue](https://github.com/Daivik1520/gesture-driver/issues) or create a [pull request](https://github.com/Daivik1520/gesture-driver/pulls).

---

## 📬 Contact

**Author:** Daivik Reddy  
- 🌐 [LinkedIn](https://www.linkedin.com/in/daivik1520/)
- ✉️ Email: daivik1520@gmail.com  
- 🐙 [GitHub](https://github.com/Daivik1520)

---

> _Gesture Driver: Hands-on control for the next generation of gaming and interactive experiences!_
