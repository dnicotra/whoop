#!/usr/bin/env python3
"""
Simple Tkinter Audio Recording Application

This application provides a GUI with:
- A text field to enter a name
- A button to start the recording process
- A countdown timer before recording starts
- 5-second audio recording capability
- Saves recordings with the provided name

Cross-platform compatible: Windows, macOS, Linux
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import wave
import sounddevice as sd
import numpy as np
import os
import platform
import re
from datetime import datetime


class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Recording parameters
        self.sample_rate = 44100  # Hz
        self.duration = 5  # seconds
        self.countdown_time = 3  # seconds
        self.recording_data = None
        self.is_recording = False
        
        # Check audio device availability on startup
        self.check_audio_devices()
        
        self.setup_ui()
        
    def check_audio_devices(self):
        """Check if audio input devices are available"""
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            
            if not input_devices:
                # Show warning but don't prevent startup
                system_name = platform.system()
                if system_name == "Windows":
                    warning_msg = ("No audio input devices detected.\n\n"
                                 "On Windows, make sure:\n"
                                 "• Your microphone is connected and enabled\n"
                                 "• Windows has microphone permissions for Python\n" 
                                 "• Check Windows Sound settings")
                else:
                    warning_msg = ("No audio input devices detected.\n"
                                 "Please check your microphone connection and system audio settings.")
                
                messagebox.showwarning("Audio Device Warning", warning_msg)
                
        except Exception as e:
            messagebox.showwarning("Audio System Warning", 
                                 f"Could not check audio devices: {str(e)}\n"
                                 "Recording may not work properly.")
        
    def sanitize_filename(self, filename):
        """Sanitize filename for cross-platform compatibility, especially Windows"""
        # Remove or replace invalid characters for Windows filenames
        # Invalid characters: < > : " | ? * \ /
        invalid_chars = r'<>:"|?*\/'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
            
        # Remove leading/trailing dots and spaces (Windows issue)
        filename = filename.strip('. ')
        
        # Ensure filename is not empty
        if not filename:
            filename = "recording"
            
        # Windows reserved names
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                         'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                         'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        
        if filename.upper() in reserved_names:
            filename = f"user_{filename}"
            
        return filename
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio Recorder", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Name input
        name_label = ttk.Label(main_frame, text="Your Name:")
        name_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, 
                                   width=30, font=("Arial", 11))
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status display
        self.status_var = tk.StringVar(value="Enter your name and click 'Start Recording'")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Arial", 10))
        status_label.grid(row=2, column=0, columnspan=2, pady=(20, 10))
        
        # Countdown display
        self.countdown_var = tk.StringVar(value="")
        self.countdown_label = ttk.Label(main_frame, textvariable=self.countdown_var, 
                                        font=("Arial", 24, "bold"), 
                                        foreground="red")
        self.countdown_label.grid(row=3, column=0, columnspan=2, pady=(10, 20))
        
        # Record button
        self.record_button = ttk.Button(main_frame, text="Start Recording", 
                                       command=self.start_recording_process)
        self.record_button.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # Progress bar for recording
        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        # Instructions
        instructions = ("Instructions:\n"
                       "1. Enter your name in the text field\n"
                       "2. Click 'Start Recording'\n"
                       "3. Wait for the countdown to finish\n"
                       "4. Recording will start automatically for 5 seconds\n"
                       "5. File will be saved with your name")
        
        instructions_label = ttk.Label(main_frame, text=instructions, 
                                      font=("Arial", 9), 
                                      justify=tk.LEFT)
        instructions_label.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
    def start_recording_process(self):
        """Start the recording process with countdown"""
        name = self.name_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter your name first!")
            return
            
        if self.is_recording:
            messagebox.showinfo("Info", "Recording is already in progress!")
            return
        
        # Disable the button and start the process
        self.record_button.config(state='disabled')
        
        # Start countdown and recording in a separate thread
        thread = threading.Thread(target=self.recording_thread)
        thread.daemon = True
        thread.start()
        
    def recording_thread(self):
        """Handle countdown and recording in a separate thread"""
        try:
            # Countdown phase
            self.status_var.set("Get ready! Recording will start in...")
            
            for i in range(self.countdown_time, 0, -1):
                self.countdown_var.set(str(i))
                time.sleep(1)
                
            self.countdown_var.set("")
            
            # Recording phase
            self.status_var.set("🔴 RECORDING... Speak now!")
            self.is_recording = True
            
            # Start progress bar
            self.progress['maximum'] = self.duration * 10  # Update every 0.1 seconds
            self.progress['value'] = 0
            
            # Record audio
            self.recording_data = sd.rec(int(self.duration * self.sample_rate), 
                                       samplerate=self.sample_rate, 
                                       channels=1, dtype=np.float32)
            
            # Update progress bar during recording
            for i in range(self.duration * 10):
                time.sleep(0.1)
                self.progress['value'] = i + 1
                
            sd.wait()  # Wait until recording is finished
            
            # Save the recording
            self.save_recording()
            
        except Exception as e:
            messagebox.showerror("Error", f"Recording failed: {str(e)}")
        finally:
            # Reset UI
            self.is_recording = False
            self.status_var.set("Enter your name and click 'Start Recording'")
            self.countdown_var.set("")
            self.progress['value'] = 0
            self.record_button.config(state='normal')
            
    def save_recording(self):
        """Save the recorded audio to a WAV file"""
        try:
            name = self.name_var.get().strip()
            
            # Sanitize name for cross-platform filename compatibility
            safe_name = self.sanitize_filename(name) if name else "anonymous"
            
            # Create filename with timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{timestamp}.wav"
            
            # Ensure recordings directory exists with cross-platform path handling
            recordings_dir = os.path.join(os.getcwd(), "recordings")
            if not os.path.exists(recordings_dir):
                os.makedirs(recordings_dir, exist_ok=True)
                
            filepath = os.path.join(recordings_dir, filename)
            
            # Convert float32 to int16 for WAV file
            audio_data = (self.recording_data * 32767).astype(np.int16)
            
            # Write WAV file with explicit binary mode for Windows compatibility
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 2 bytes per sample (int16)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())
                
            self.status_var.set(f"✅ Recording saved as: {filename}")
            
            # Show success message with full path for clarity
            success_msg = f"Recording saved successfully!\nFile: {filename}\nLocation: {recordings_dir}"
            messagebox.showinfo("Success", success_msg)
            
        except Exception as e:
            error_msg = f"Failed to save recording: {str(e)}"
            self.status_var.set("❌ Save failed - check console")
            messagebox.showerror("Error", error_msg)


def main():
    """Main function to run the application"""
    try:
        # Handle Windows-specific DPI awareness for better GUI scaling
        if platform.system() == "Windows":
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass  # Ignore if not available
                
        root = tk.Tk()
        
        # Set window icon if available (cross-platform)
        try:
            # On Windows, this will work if there's an .ico file
            # On other platforms, it will be ignored or use a different format
            root.iconbitmap(default='audio_icon.ico')
        except:
            pass  # Ignore if icon file not found
            
        app = AudioRecorderApp(root)
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication closed by user")
            
    except Exception as e:
        # Handle any startup errors gracefully
        error_msg = f"Failed to start application: {str(e)}"
        print(error_msg)
        try:
            import tkinter.messagebox as mb
            mb.showerror("Startup Error", error_msg)
        except:
            pass


if __name__ == "__main__":
    main()