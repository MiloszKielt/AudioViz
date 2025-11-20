import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

def read_coordinates(filename):
    """Reads time and amplitude values from the text file into two arrays."""
    times, amplitudes = [], []
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    t, a = float(parts[0]), float(parts[1])
                    times.append(t)
                    amplitudes.append(a)
    except FileNotFoundError:
        print("File not found. Waiting for data...")
    return times, amplitudes

import matplotlib.widgets as widgets

t, a = read_coordinates('numbers.txt')

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Adjust the bottom to make space for the slider

graph, = ax.plot([], [], '-')

# Add greyed out horizontal line at y=0
ax.axhline(y=0, color='grey', linestyle='--')

ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = widgets.Slider(ax_slider, 'Time', 0, len(t)-1, valinit=0, valstep=1)

def animate(i):
    start = max(0, i - 60)
    end = i + 1
    graph.set_data(t[start:end], a[start:end])
    ax.set_xlim(t[start], t[end-1])
    ax.set_ylim(min(a) - 0.1 * abs(min(a)), max(a) + 0.1 * abs(max(a)))
    return graph

def update(val):
    frame = int(slider.val)
    animate(frame)

slider.on_changed(update)

ani = FuncAnimation(fig, animate, frames=len(t), interval=1000/60)  # 1000 ms / 60 fps
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Waveform')
plt.show()
