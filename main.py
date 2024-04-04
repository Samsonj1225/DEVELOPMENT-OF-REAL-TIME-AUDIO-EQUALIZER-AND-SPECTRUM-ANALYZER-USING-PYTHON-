import numpy as np
import sounddevice as sd
from scipy.signal import firwin, welch
import matplotlib.pyplot as plt

# Define parameters
Fs = 44100         # Sampling frequency
NFFT = 1024        # FFT length
duration = 5       # Recording duration in seconds

# Define equalizer parameters
equalizer_gain = [1, 1.5, 0.8, 1.2, 0.9]   # Gain for each frequency band
equalizer_freqs = [100, 500, 1000, 5000, 10000]  # Center frequencies of each band

# Create audio input object
print('Start speaking.')
audio_data = sd.rec(int(duration * Fs), samplerate=Fs, channels=1, dtype='float32')
sd.wait()
print('End of Recording.')

# Design FIR filter for equalization
nyquist = 0.45 * Fs  # Adjusted Nyquist frequency
bands = [0] + [f / nyquist for f in equalizer_freqs] + [1]
equalizer_filter = firwin(NFFT // 2 + 1, bands[1:-1], pass_zero=False)

# Apply equalization to audio data
equalized_audio = np.convolve(audio_data[:, 0], equalizer_filter, mode='same')

# Compute spectrum of equalized audio
f, S = welch(equalized_audio, Fs, nperseg=NFFT, window='hamming', scaling='density')

# Plot spectrum
plt.figure()
plt.semilogx(f, 10 * np.log10(S))
plt.title('Equalized Audio Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.show()

# Play equalized audio
print('Playing equalized audio...')
sd.play(equalized_audio, Fs)
sd.wait()
