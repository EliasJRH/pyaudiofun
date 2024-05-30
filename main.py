import wave
import numpy as np
from scipy import signal

def main():
    wave_obj = wave.open("Gravity Falls.wav", "rb")
    samples_per_sec = wave_obj.getframerate()
    samples = wave_obj.getnframes()
    length = samples/samples_per_sec
    print(f"{samples}/{samples_per_sec}={length}")
    print(samples_per_sec * 0.1)
    signalwave = wave_obj.readframes(samples)
    signal_array = np.frombuffer(signalwave, dtype=np.int16)
    times = np.linspace(0, samples/samples_per_sec, num=samples)
    print(times)
    print([1,2,3])
    peaks_indices = signal.find_peaks(signal_array)
    print(peaks_indices[0])
    peak_times = []
    for i in list(peaks_indices[0][0:20]):
        peak_times.append(times[i])

    print(peak_times)




if __name__ == "__main__":
    main()
