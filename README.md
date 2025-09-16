# Audio Recorder Application

A simple Python GUI application using tkinter for recording audio with a countdown timer.

## Features

- Simple GUI with name input field and recording button
- 3-second countdown before recording starts
- 5-second audio recording
- Saves recordings as WAV files with the provided name and timestamp
- Creates a `recordings/` directory for storing audio files

## Requirements

- Python 3.12+
- tkinter (usually comes with Python)
- sounddevice
- numpy
- portaudio (system dependency)

## Installation

1. Install system dependencies (Ubuntu/Debian):
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

### How to use:
1. Enter your name in the text field
2. Click "Start Recording"
3. Wait for the 3-second countdown
4. Speak for 5 seconds when recording starts
5. The recording will be saved automatically in the `recordings/` directory

## File Structure

- `audio_recorder.py` - Main application file
- `requirements.txt` - Python dependencies
- `recordings/` - Directory where audio files are saved (created automatically)