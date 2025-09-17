# Audio Recorder Application

A simple Python GUI application using tkinter for recording audio with a countdown timer.

## Features

- Simple GUI with name input field and recording button
- **Configurable recording duration (1-30 seconds)**
- 3-second countdown before recording starts
- **Real-time volume level monitoring**
- **Audio playback of recorded files**
- **Recording list with file management**
- **Delete recordings functionality**
- Saves recordings as WAV files with the provided name and timestamp
- Creates a `recordings/` directory for storing audio files
- **Enhanced user interface with intuitive controls**
- **Cross-platform compatible: Windows, macOS, Linux**

## Requirements

- Python 3.8+ (Python 3.12+ recommended)
- tkinter (usually comes with Python)
- sounddevice
- numpy
- System audio dependencies (see installation below)

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
sudo apt install python3-tk pulseaudio portaudio19-dev
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
2. **Choose your preferred recording duration (1-30 seconds)**
3. **Watch the volume meter to ensure your microphone is working**
4. Click "Start Recording"
5. Wait for the 3-second countdown
6. **Speak for the selected duration when recording starts**
7. The recording will be saved automatically in the `recordings/` directory
8. **Click "Play Last Recording" to listen to your recording**
9. **View all recordings in the list below**
10. **Double-click any recording in the list to play it**
11. **Select recordings and use "Delete Selected" to remove unwanted files**

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

### General Issues

**"ModuleNotFoundError" for sounddevice or numpy:**
```cmd
pip install --upgrade sounddevice numpy
```

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

## New Features

### 🎵 Audio Playback
- Play back your recordings immediately after saving
- "Play Last Recording" button becomes available after first recording
- Safe playback with proper thread handling
- Prevents multiple simultaneous playbacks

### ⏱️ Configurable Recording Duration
- Choose recording length from 1 to 30 seconds
- Default remains 5 seconds for familiar experience
- Progress bar automatically adjusts to selected duration
- Clear visual feedback during recording

### 🎨 Enhanced User Interface
- Larger window (600x500) for better layout
- Side-by-side record and playback buttons
- Clear duration selection with spinbox control
- Updated instructions reflecting all features

### 📂 Recording Management
- View all recordings in an organized list
- See recording names and timestamps
- Double-click recordings to play them instantly
- Select and delete unwanted recordings
- Automatic loading of existing recordings on startup
- Safe deletion with confirmation dialogs

### 📊 Volume Level Monitoring
- Real-time volume meter shows microphone input levels
- Visual feedback before and during recording
- Helps ensure optimal recording conditions
- Background monitoring when not recording
- Automatic scaling for different microphone sensitivities