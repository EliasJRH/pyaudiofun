import wave
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def main():
    # Create a wave object from the file
    wav_obj = wave.open("Gravity Falls.wav", "rb")

    # Obtain number of samples per second and number of samples
    samples_per_sec = wav_obj.getframerate()
    samples = wav_obj.getnframes()
    channels = wav_obj.getnchannels()

    # From the number of samples and samples per second, calculate the length of the audio file
    length = samples / samples_per_sec

    # print(f"{samples}/{samples_per_sec}={length}")
    # print(samples_per_sec * 0.1)

    # Read the wave object and convert it to a numpy array
    signalwave = wav_obj.readframes(samples)
    signal_array = np.frombuffer(signalwave, dtype=np.int16)

    # Get the left and right channels
    l_channel = signal_array[::2]
    r_channel = signal_array[1::2]

    # Obtain the time values for the x-axis
    times = np.linspace(0, samples / samples_per_sec, num=samples)

    peaks_indices_left = signal.find_peaks(l_channel, prominence=1)[0]
    # l_channel_and_times = list(zip(l_channel, times_left))
    peak_times = []
    peak_values = []
    for i in list(peaks_indices_left):
        if i >= len(l_channel):
            break
        peak_times.append(times[i])
        peak_values.append(l_channel[i])

    # Plot the signal
    plt.figure(figsize=(15, 5))
    plt.plot(times, l_channel)
    plt.plot(peak_times, peak_values, "ro")
    plt.title("Left channel")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.xlim(0, length)
    plt.show()

    # print(times)
    # print([1,2,3])
    # peaks_indices = signal.find_peaks(signal_array)
    # print(peaks_indices[0])
    # peak_times = []
    # for i in list(peaks_indices[0][0:20]):
    #     peak_times.append(times[i])


if __name__ == "__main__":
    main()
