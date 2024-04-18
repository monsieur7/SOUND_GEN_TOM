import numpy as np
import pyaudio
from scipy import signal

# Parameters
fs = 44100
freq = 440  # Initial frequency in Hz
dt = 0.01  # Duration of each frequency segment in seconds

# PyAudio callback function
def audio_callback(in_data, frame_count, time_info, status):
    global freq, dt, fs
    
    # Generate audio samples based on the current frequency
    t = np.linspace(0, dt, int(fs * dt), endpoint=False)
    samples = np.sin(2 * np.pi * t * freq)

    # Scale samples to float32 and write to output stream
    data = (samples * 0.5).astype(np.float32).tobytes()
    print(f"Frequency: {freq} Hz")

    return data, pyaudio.paContinue

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open PyAudio stream in callback mode
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True,
                stream_callback=audio_callback)

# Start the stream
stream.start_stream()

# Keep the stream active
try:
    while stream.is_active():
        continue
except KeyboardInterrupt:
    # Close the stream gracefully
    stream.stop_stream()
    stream.close()
    p.terminate()
