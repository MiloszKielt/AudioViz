import wave
import numpy as np
import sys

def read_wav_file(filename, target_samples_per_second=100):
    with wave.open(filename, 'rb') as wav_file:
        # Extract basic parameters
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        
        # Read frames and convert to numpy array
        frames = wav_file.readframes(n_frames)
        dtype = np.int16 if sample_width == 2 else np.uint8  # Handle 16-bit and 8-bit PCM
        samples = np.frombuffer(frames, dtype=dtype)
        
        # If stereo, take only one channel
        if n_channels > 1:
            samples = samples[::n_channels]
        
        # Calculate step to achieve target samples per second
        step = max(1, framerate // target_samples_per_second)
        
        # Downsample by taking every nth sample
        samples = samples[::step]
        time_values = np.linspace(0, n_frames / framerate, num=len(samples))
        
        return time_values, samples

def save_coordinates_to_file(time_values, samples, output_filename):
    with open(output_filename, 'w') as f:
        for t, s in zip(time_values, samples):
            f.write(f"{t:.6f} {s}\n")

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input.wav> <output.txt> [step]")
        sys.exit(1)
    
    input_wav = sys.argv[1]
    output_txt = sys.argv[2]
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 100  # Default step to 100
    
    time_values, samples = read_wav_file(input_wav, step)
    
    # Normalize samples to [-1.1, 1.1]
    max_val = np.max(np.abs(samples))
    samples = samples / max_val * 1.1
    save_coordinates_to_file(time_values, samples, output_txt)
    print(f"Coordinates saved to {output_txt} (downsampled with step {step})")

if __name__ == "__main__":
    main()