import tkinter as tk
from tkinter import messagebox
import numpy as np
import sounddevice as sd
from scipy.signal import firwin, welch
import matplotlib.pyplot as plt
import threading

# Parameters
Fs = 44100
NFFT = 1023
recording = False
audio_data = []
equalized_audio = None

# Equalizer settings
equalizer_freqs = [100, 500, 1000, 5000, 10000]

def audio_callback(indata, frames, time, status):
    if recording:
        audio_data.append(indata.copy())

def start_recording():
    global recording, audio_data, stream
    if recording:
        return
    recording = True
    audio_data.clear()
    status_label.config(text="🎙️ Recording...")
    stream = sd.InputStream(samplerate=Fs, channels=1, callback=audio_callback)
    stream.start()

def stop_recording():
    global recording, stream
    if not recording:
        return
    recording = False
    stream.stop()
    stream.close()
    status_label.config(text="🛑 Recording stopped.")
    messagebox.showinfo("Done", "Recording stopped! You may now visualize or play.")

def process_audio():
    global equalized_audio
    if not audio_data:
        messagebox.showwarning("Warning", "No recorded audio found.")
        return
    recorded = np.concatenate(audio_data, axis=0).flatten()
    nyquist = 0.5 * Fs
    bands = [f / nyquist for f in equalizer_freqs]
    eq_filter = firwin(NFFT, bands, pass_zero=False)
    equalized_audio = np.convolve(recorded, eq_filter, mode='same')
    f, S = welch(equalized_audio, Fs, nperseg=NFFT, window='hamming', scaling='density')
    plt.figure(figsize=(8, 4))
    plt.semilogx(f, 10 * np.log10(S))
    plt.title('Equalized Audio Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def play_audio():
    if equalized_audio is None:
        messagebox.showwarning("Warning", "Please process audio first.")
        return
    gain = volume_scale.get()
    amplified = np.clip(equalized_audio * gain, -1.0, 1.0)
    sd.play(amplified, Fs)
    status_label.config(text="🔊 Playing equalized audio...")

# GUI
root = tk.Tk()
root.title("🎛️ Real-Time Audio Equalizer")
root.geometry("420x400")
root.configure(bg="#202030")

tk.Label(root, text="Audio Equalizer & Spectrum Analyzer", font=("Arial", 14, "bold"), fg="white", bg="#202030").pack(pady=10)

tk.Button(root, text="🎙️ Start Speaking", command=start_recording, width=30, bg="#304070", fg="white", font=("Arial", 10)).pack(pady=5)
tk.Button(root, text="🛑 Stop Speaking", command=stop_recording, width=30, bg="#804040", fg="white", font=("Arial", 10)).pack(pady=5)
tk.Button(root, text="📊 Show Equalized Audio Spectrum", command=process_audio, width=30, bg="#406080", fg="white", font=("Arial", 10)).pack(pady=5)
tk.Button(root, text="🔊 Play Equalized Audio", command=play_audio, width=30, bg="#208060", fg="white", font=("Arial", 10)).pack(pady=5)

volume_scale = tk.Scale(root, from_=0.5, to=3.0, resolution=0.1, orient="horizontal", label="Volume Boost", bg="#202030", fg="white")
volume_scale.set(1.5)
volume_scale.pack(pady=10)

status_label = tk.Label(root, text="", fg="lightgreen", bg="#202030", font=("Arial", 10))
status_label.pack(pady=10)

root.mainloop()
