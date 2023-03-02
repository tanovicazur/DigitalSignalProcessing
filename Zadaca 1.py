import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_wav("bells.wav")
#play(song)
samplerate, data = wavfile.read("bells.wav")

n = np.arange(0, 1, 1/len(data))

noise = np.random.normal(0, 1, len(data))

plt.figure(),
plt.plot(n, data)
plt.title("Audio signal")
plt.grid()

plt.figure(),
plt.plot(n, noise, 'r')
plt.title("AWGN")
plt.grid()

prevData = data
data = data + noise
h = np.array([-0.015, 0.058, -0.350, 1.000, -0.350, 0.058, -0.005])
y = np.convolve(data, h, mode = 'same');

plt.figure(),
plt.plot(n, prevData, 'g')
plt.title("Audio signal without AWGN")
plt.grid()

plt.figure(),
plt.plot(n, data)
plt.title("Audio signal with AWGN")
plt.grid()

plt.figure(),
plt.plot(n, y, 'r')
plt.title("Audio signal with AWGN and disipation")
plt.grid()
