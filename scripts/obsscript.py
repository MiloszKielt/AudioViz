import numpy as np
import matplotlib.pyplot as plt
import time
import pyaudio

import struct
from tkinter import TclError


# Parameters
CHUNK = 1024 * 4  # Increased chunk size for better performance
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1000

# Initialize PyAudio
p = pyaudio.PyAudio()

# List available devices
print("Available audio devices:")
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"{i}: {dev['name']} (max inputs: {dev['maxInputChannels']})")

# Try to find Stereo Mix device
stereo_mix_index = None
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if "stereo mix" in dev['name'].lower():
        stereo_mix_index = i
        break

if stereo_mix_index is None:
    print("Stereo Mix not found. Trying default input device...")
    stereo_mix_index = p.get_default_input_device_info()['index']

# Open stream
try:
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=2,
        frames_per_buffer=CHUNK
    )
    print(f"Using device {stereo_mix_index}: {p.get_device_info_by_index(stereo_mix_index)['name']}")
except Exception as e:
    print(f"Error opening stream: {e}")
    p.terminate()
    exit()

# Setup visualization
fig, ax = plt.subplots(1, figsize=(16, 9))
x = np.arange(0, CHUNK)
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

ax.set_title('AUDIO VISUALIZER')
ax.set_ylim(-32768//2, 32767//2)
ax.set_xlim(0, CHUNK)
ax.axis('off')
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.margins(0)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
line.set_color('white')

plt.show(block=False)

frame_count = 0
start_time = time.time()

print("Starting visualization...")
try:
    while True:
        # Read audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        
        # Convert to numpy array
        data_np = np.frombuffer(data, dtype=np.int16)
        
        # If stereo, take only one channel
        if CHANNELS == 2:
            data_np = data_np[::2]
        
        # Update plot
        line.set_ydata(data_np)
        
        # Change color periodically
        if frame_count % 10 == 0:
            line.set_color('cyan')
        elif frame_count % 5 == 0:
            line.set_color('magenta')
        else:
            line.set_color('white')
        
        # Update display
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
except KeyboardInterrupt:
    print("\nStopping visualization...")
except TclError:
    print("Window closed.")
except Exception as e:
    print(f"Error: {e}")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Done.")