# Audio Recorder Application

A simple Python GUI application using tkinter for recording audio with a countdown timer.

## Features

- Simple GUI with name input field and recording button
- 3-second countdown before recording starts
- 5-second audio recording
- **5-second webcam video recording (when webcam is available)**
- Saves recordings as WAV (audio) and MP4 (video) files with the provided name and timestamp
- Creates a `recordings/` directory for storing both audio and video files
- **Cross-platform compatible: Windows, macOS, Linux**

## Requirements

- Python 3.8+ (Python 3.12+ recommended)
- tkinter (usually comes with Python)
- sounddevice
- numpy
- opencv-python (for webcam recording)
- System audio and video dependencies (see installation below)

## Installation

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/) if not already installed
   - Make sure to check "Add Python to PATH" during installation

2. Install Python dependencies:
```cmd
pip install -r requirements.txt
```

3. **Audio System Setup:**
   - Ensure your microphone is connected and working
   - Check Windows Sound settings (Right-click sound icon → "Open Sound settings")
   - Make sure microphone privacy settings allow desktop apps to access microphone
   - Go to Settings → Privacy & Security → Microphone → "Let desktop apps access your microphone"

### macOS

1. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

2. Audio permissions may be requested when first running the app

### Linux (Ubuntu/Debian)

1. Install system dependencies:
```bash
sudo apt update
sudo apt install python3-tk python3-opencv python3-numpy pulseaudio portaudio19-dev
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

Run the application:
```bash
python3 audio_recorder.py
```

On Windows, you can also use:
```cmd
python audio_recorder.py
```

### How to use:
1. Enter your name in the text field
2. Click "Start Recording"
3. Wait for the 3-second countdown
4. Speak and look at the camera for 5 seconds when recording starts
5. Both audio (.wav) and video (.mp4) files will be saved automatically in the `recordings/` directory

**Note:** If no webcam is detected, the application will run in audio-only mode.

## Troubleshooting

### Windows-Specific Issues

**"No audio input devices detected":**
- Check that your microphone is plugged in and recognized by Windows
- Go to Settings → System → Sound → Input → Make sure your microphone is listed and working
- Test your microphone using Windows Voice Recorder app first

**"Recording failed" errors:**
- Ensure Python has microphone permissions
- Go to Settings → Privacy & Security → Microphone → Allow desktop apps
- Try running as administrator if permission issues persist
- Check that no other applications are using the microphone exclusively

**GUI scaling issues on high-DPI displays:**
- The app includes DPI awareness for better scaling on Windows
- If text appears too small/large, check Windows display scaling settings

**Permission errors when saving files:**
- Make sure the application has write permissions in its directory
- Try running from a folder in your user directory (not Program Files)

**"No webcam detected" warning:**
- Ensure your webcam is connected and not in use by other applications
- Check Windows camera permissions: Settings → Privacy & Security → Camera
- Test your camera with the Windows Camera app first

### General Issues

**"ModuleNotFoundError" errors:**
- For pip-installed packages: `pip install --upgrade sounddevice`
- For system packages on Linux: `sudo apt install python3-opencv python3-numpy`

**Webcam issues:**
- Close other applications that might be using the camera (Zoom, Skype, etc.)
- Try unplugging and reconnecting USB cameras
- Check camera permissions in your operating system settings

**Audio latency or quality issues:**
- Close other audio applications
- Check system audio settings and sample rate
- Try different microphone input sources

## File Structure

- `audio_recorder.py` - Main application file with cross-platform compatibility
- `requirements.txt` - Python dependencies
- `run_windows.bat` - Windows batch file for easy startup (double-click to run)
- `test_windows_compatibility.py` - Windows compatibility testing script
- `recordings/` - Directory where audio files are saved (created automatically)

## Windows-Specific Features

This application includes several Windows-specific enhancements:

- **DPI Awareness**: Automatic high-DPI display scaling support
- **Filename Sanitization**: Handles Windows reserved names (CON, PRN, etc.) and invalid characters
- **Audio Permission Checking**: Detects and provides guidance for microphone permission issues
- **Batch File Launcher**: `run_windows.bat` for easy startup without command line
- **Windows Path Handling**: Proper directory creation and file path management
- **Error Handling**: Windows-specific error messages and troubleshooting guidance

The application has been tested for Windows compatibility and includes specific handling for common Windows issues.