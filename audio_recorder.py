#!/usr/bin/env python3
"""
Simple Tkinter Audio Recording Application

This application provides a GUI with:
- A text field to enter a name
- A button to start the recording process
- A countdown timer before recording starts
- 5-second audio recording capability
- Saves recordings with the provided name
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import wave
import sounddevice as sd
import numpy as np
import os
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
        
        self.setup_ui()
        
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
            
            # Create filename with timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.wav"
            
            # Ensure recordings directory exists
            if not os.path.exists("recordings"):
                os.makedirs("recordings")
                
            filepath = os.path.join("recordings", filename)
            
            # Convert float32 to int16 for WAV file
            audio_data = (self.recording_data * 32767).astype(np.int16)
            
            # Write WAV file
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 2 bytes per sample (int16)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data.tobytes())
                
            self.status_var.set(f"✅ Recording saved as: {filename}")
            messagebox.showinfo("Success", f"Recording saved successfully!\nFile: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save recording: {str(e)}")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = AudioRecorderApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user")


if __name__ == "__main__":
    main()