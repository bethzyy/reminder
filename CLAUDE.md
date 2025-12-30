# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pomodoro Timer (番茄闹钟) desktop application built with Python and web technologies. The app uses `pywebview` to create a native desktop window that displays a web-based timer interface.

## Architecture

### Backend (Python + pywebview)
The app runs a local HTTP server dynamically allocated on a free port, then creates a native window via pywebview pointing to that local server.

**app.py** contains:
- `Api` class: Exposes Python methods to JavaScript via `js_api` parameter (currently provides `log()` method for writing to tomato.log)
- `find_free_port()`: Dynamically finds available port using socket binding
- `start_server()`: Spawns HTTP server in daemon thread serving static files via SimpleHTTPRequestHandler
- `main()`: Orchestrates server startup, creates pywebview window, shuts down server on exit

Key architectural detail: The HTTP server changes to the script's directory (`os.chdir`) before starting, so relative paths work correctly.

### Frontend (JavaScript)
**script.js** contains a single `PomodoroTimer` class that manages all UI logic:
- State management via instance properties (`isRunning`, `isPaused`, `remainingSeconds`, etc.)
- LocalStorage integration: Saves/restores time value and unit preference
- `log()` method: Writes logs to console and delegates to `window.pywebview.api.log()` for file logging
- `playAlarm()`: Uses Web Audio API (OscillatorNode + GainNode) to create a 3-second melody with C major pentatonic scale

The frontend communicates with Python backend through `window.pywebview.api` (e.g., for logging).

### Build System (PyInstaller)
**PomodoroTimer_optimized.spec** defines the executable build:
- Data files: `index.html`, `style.css`, `script.js` are bundled into the executable
- Exclusions: Removes tkinter, numpy, pandas, matplotlib, GUI frameworks (PyQt/PySide), web frameworks (flask/django) to minimize size
- Console-less: `console=False` for silent execution
- UPX compression enabled for smaller binary

After building, the executable extracts bundled HTML/CSS/JS to a temp directory at runtime.

## Common Commands

### Development
```bash
# Run from source (uses latest code)
python app.py

# After code changes, rebuild executable to test:
python -m PyInstaller PomodoroTimer_optimized.spec --clean
```

### Dependencies
```bash
pip install pywebview pyinstaller
```

### Testing Audio
The alarm melody plays automatically when timer finishes. To test quickly without waiting, set timer to 5-10 seconds.

## Key Technical Details

- **Dynamic port allocation**: Server finds free port at runtime; no hardcoded ports or conflicts
- **State persistence**: Uses localStorage with keys `pomodoroTime` and `pomodoroUnit`
- **Audio implementation**: Web Audio API creates 7-note sequence (C5→D5→E5→G5→E5→C5→G5) using sine oscillators with exponential gain ramp (0.3 to 0.01 over 3 seconds)
- **Window constraints**: 300x320px fixed size, non-resizable, min_size 240x280px
- **Executable size**: ~17MB after UPX compression (spec file excludes ~20 common Python packages)
- **Logging**: JavaScript can call `window.pywebview.api.log(message)` to write to `tomato.log` in app directory

## File Locations

- Built executable: `dist/PomodoroTimer.exe`
- Source files: `app.py`, `index.html`, `style.css`, `script.js`
- Build config: `PomodoroTimer_optimized.spec`, `build_app.bat`
- Log file: `tomato.log` (created at runtime)
