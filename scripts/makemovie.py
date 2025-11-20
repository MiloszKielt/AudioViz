import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import pyaudio
import argparse
from tkinter import TclError

parser = argparse.ArgumentParser(description='Visualize a WAV file')
parser.add_argument('file', default=None, type=str, help='The WAV file to visualize [Provide in format: <filename>.wav]')

args = parser.parse_args()

if args.file is None:
    print('No file provided. Exiting...')
    exit(1)

# Open the WAV file
print(f"Reading file: {args.file}")
wav_file = wave.open(args.file, 'rb')

# Some parameters for the WAV file
CHUNK = 1024 * 2
CHANNELS = wav_file.getnchannels()
RATE = wav_file.getframerate()
WIDTH = wav_file.getsampwidth()

# Open stream to play audio
print('Opening audio stream')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True)


print('Configuring plots')
# Create the figure and axis
fig, ax = plt.subplots(1, figsize=(16, 9))
x = np.arange(0, CHUNK, 1)

line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# Configure the look of the plot
ax.set_title('WAVEFORM VIZ')
ax.set_ylim(-32768, 32767)   # Adjusted for 16-bit audio range
ax.set_xlim(0, CHUNK)

ax.axis('off')
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
ax.margins(0)

fig.patch.set_facecolor('black')
ax.set_facecolor('black')
line.set_color('white')

ax.set_xticks([0, CHUNK // 2, CHUNK])

# show the plot
plt.show(block=False)

# for measuring frame rate
frame_count = 0
start_time = time.time()

# Set initial position to the 30th minute
# initial_position = 30 * 60 * RATE * CHANNELS * WIDTH
# wav_file.setpos(initial_position // (CHANNELS * WIDTH))

print("Playing vizualization...")
while True:
    # Read binary data from audio file
    data = wav_file.readframes(CHUNK)


    if len(data) == 0:
        break
    
    # Play the audio
    stream.write(data)

    data_np = np.array(struct.unpack('<' + ('h' * (len(data) // 2)), data), dtype=np.int16)[::2]
    line.set_ydata(data_np)
    
    # update canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        # Threshold analysis for low sounds
        low_threshold = 2048
        low_count = np.sum(np.abs(data_np) < low_threshold)
        low_ratio = low_count / (len(data_np) / 2) / 2

        # Color adjustment based on low sound ratio
        blue_intensity = max(0.3, low_ratio)
        line.set_color((abs(blue_intensity / 2), 0, max(0.7 , abs(blue_intensity - 1))))

        # line.set_color((abs(blue_intensity / 2), 0, max(0.5 , abs(blue_intensity - 1))))
        
        
        # if low_ratio < 0.5:
        #     # Map low ratio to blue gradient (darker blue for lower ratios)
        #     blue_intensity = max(0.3, low_ratio)  # Ensure minimum visibility
        #     line.set_color((0, 0, blue_intensity))
        # elif low_ratio < 1.5:
        #     line.set_color('cyan')
        # else:
        #     line.set_color('yellow')
        # if(frame_count % 10 == 0):
        #     line.set_color('white')
        # elif(frame_count % 5 == 0):
        #     line.set_color('black')
        
        frame_count += 1
    except TclError:
        print('stream stopped')
        break

print('Closing audio stream')
wav_file.close()
stream.stop_stream()
stream.close()
p.terminate()

print('Process finished')