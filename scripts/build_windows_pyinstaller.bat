@echo off
setlocal

REM Build GestureRacer.exe on Windows using PyInstaller
REM Requirements: Python 3.11, Internet access to install dependencies

where python >nul 2>&1
IF ERRORLEVEL 1 (
  echo Python not found in PATH. Please install Python 3.11 and ensure 'python' is available.
  exit /b 1
)

echo Creating venv...
python -m venv .venv
call .venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo Installing project dependencies...
pip install -r requirements.txt

echo Installing PyInstaller...
pip install pyinstaller

echo Converting PNG icon to ICO...
pip install pillow
IF NOT EXIST assets\icon.png (
  echo Please copy your icon PNG to assets\icon.png and rerun.
  exit /b 1
)
python scripts\make_icon.py

echo Building executable (GestureRacer.exe)...
pyinstaller --clean --noconfirm build\pyinstaller_win.spec

IF %ERRORLEVEL% NEQ 0 (
  echo Build failed.
  exit /b %ERRORLEVEL%
)

echo Build complete. Executable located at: dist\GestureRacer.exe
pause