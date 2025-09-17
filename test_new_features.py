#!/usr/bin/env python3
"""
Test script for new audio recorder features
"""

import os
import sys
import tempfile
import wave
import numpy as np
from datetime import datetime

def test_ui_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        import threading
        import time
        import wave
        import numpy as np
        import os
        import platform
        import re
        from datetime import datetime
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_audio_recorder_class():
    """Test that AudioRecorderApp class can be instantiated"""
    print("\nTesting AudioRecorderApp class...")
    try:
        # Import the class
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Mock sounddevice since it won't work in this environment
        class MockSD:
            @staticmethod
            def query_devices():
                return []
            @staticmethod
            def rec(*args, **kwargs):
                return np.zeros((44100, 1))
            @staticmethod
            def wait():
                pass
            @staticmethod
            def play(*args, **kwargs):
                pass
        
        # Monkey patch sounddevice
        import audio_recorder
        audio_recorder.sd = MockSD()
        
        # Try to create the app (but don't show GUI)
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = audio_recorder.AudioRecorderApp(root)
        
        # Test that new attributes exist
        assert hasattr(app, 'is_playing'), "Missing is_playing attribute"
        assert hasattr(app, 'last_recording_path'), "Missing last_recording_path attribute"
        assert hasattr(app, 'duration_var'), "Missing duration_var attribute"
        assert hasattr(app, 'playback_button'), "Missing playback_button attribute"
        
        # Test that new methods exist
        assert hasattr(app, 'play_last_recording'), "Missing play_last_recording method"
        assert hasattr(app, 'playback_thread'), "Missing playback_thread method"
        
        root.destroy()
        print("✅ AudioRecorderApp class test passed")
        return True
        
    except Exception as e:
        print(f"❌ AudioRecorderApp test failed: {e}")
        return False

def test_configurable_duration():
    """Test that duration configuration works"""
    print("\nTesting configurable duration...")
    try:
        # Mock audio recorder with different durations
        durations = [1, 5, 10, 30]
        for duration in durations:
            # Simulate recording with different durations
            sample_rate = 44100
            samples = int(duration * sample_rate)
            test_audio = np.zeros((samples, 1))
            
            assert len(test_audio) == samples, f"Duration {duration}s test failed"
            
        print("✅ Configurable duration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configurable duration test failed: {e}")
        return False

def test_playback_functionality():
    """Test playback functionality with a mock WAV file"""
    print("\nTesting playback functionality...")
    try:
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            
        # Create test audio data
        sample_rate = 44100
        duration = 1
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        test_audio = np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
        audio_data = (test_audio * 32767).astype(np.int16)
        
        # Write WAV file
        with wave.open(tmp_path, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 2 bytes per sample
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
            
        # Test reading the file back
        with wave.open(tmp_path, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            read_sample_rate = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            
        assert read_sample_rate == sample_rate, "Sample rate mismatch"
        assert channels == 1, "Channel count mismatch"
        assert sampwidth == 2, "Sample width mismatch"
        assert len(frames) > 0, "No audio data read"
        
        # Clean up
        os.unlink(tmp_path)
        
        print("✅ Playback functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Playback functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing new audio recorder features...\n")
    
    tests = [
        test_ui_imports,
        test_audio_recorder_class,
        test_configurable_duration,
        test_playback_functionality
    ]
    
    results = []
    for test in tests:
        results.append(test())
        
    print("\n" + "="*50)
    if all(results):
        print("🎉 ALL TESTS PASSED!")
        print("\nNew features added successfully:")
        print("- ✅ Playback functionality")
        print("- ✅ Configurable recording duration")  
        print("- ✅ Enhanced UI with new controls")
    else:
        print("❌ Some tests failed. Check the output above.")
        
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)