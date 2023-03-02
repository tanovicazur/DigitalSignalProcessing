import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play

def echo(signal, numberOfEchoes = 5, echoStartPoint = 4000):
    dif = echoStartPoint*numberOfEchoes
    extendedSignal = np.concatenate((signal, np.zeros(dif)))
    delayedSignal = signal
    for i in range(1, numberOfEchoes + 1):
        delayedSignal = np.concatenate((np.zeros(echoStartPoint), delayedSignal))
        delayedSignal = delayedSignal/(3*i)
        extendedSignal = extendedSignal + np.concatenate((delayedSignal, np.zeros(dif - i*echoStartPoint)));
    return extendedSignal

def pitchBy(song, octaves = -0.5):
    newSamplerate = int(song.frame_rate * (2.0 ** octaves));
    songy = song._spawn(song.raw_data, overrides={'frame_rate':newSamplerate});
    return songy;

def fadeIn(songData):
    fadeEnd = 100000
    step = 1/100000
    for i in range(0, fadeEnd):
        songData[i] = np.ceil(songData[i]*step*i)
    return songData

def fadeOut(songData):
    fadeStart = len(songData) - 100000
    step = 1/100000
    for i in range(0,100000):
        songData[fadeStart + i] = np.ceil(songData[fadeStart + i]*step*(100000-i))
    return songData 

def reverse(signal):
    reversedSignal = np.zeros(len(signal))
    for i in range(0,len(signal)):
        reversedSignal[i] = signal[len(signal)-i-1]
    return reversedSignal

#DEFAULT AUDIO
song = AudioSegment.from_wav("getty.wav")
#play(song)
samplerate, data = wavfile.read('getty.wav')
t1 = np.arange(0, 1, 1/len(data));


plt.figure(),
plt.plot(t1, data);
plt.title("Default audio");
plt.grid()

#REVERSE APPLIED
reverseData = reverse(data);
wavfile.write("reverse.wav", samplerate, reverseData.astype(np.int16));
reverseSong = AudioSegment.from_wav("reverse.wav");
#play(reverseSong);

plt.figure(),
plt.plot(t1, reverseData);
plt.title("Reversed audio");
plt.grid()


#ECHO APPLIED
echoData = echo(data);
wavfile.write("echo.wav", samplerate, echoData.astype(np.int16))
echoedSong = AudioSegment.from_wav("echo.wav")
#play(echoedSong);

t2 = np.arange(0, 1, 1/len(echoData));

plt.figure(),
plt.plot(t2, echoData);
plt.title("Echoed audio");
plt.grid()

#PITCH APPLIED
pitchedSong = pitchBy(song);
pitchedData = pitchedSong.get_array_of_samples()
pitchedData = np.array(pitchedData);
play(pitchedSong);


plt.figure(),
plt.plot(t1, pitchedData);
plt.title("Pitched audio");
plt.grid()


#FADEIN AND FADEOUT APPLIED
fadeInData = fadeIn(data);
fadeInOutData = fadeOut(fadeInData);
wavfile.write("fadeInOut.wav", samplerate, fadeInOutData.astype(np.int16));
fadeInOutSong = AudioSegment.from_wav("fadeInOut.wav");
#play(fadeInOutSong);

plt.figure(),
plt.plot(t1, fadeInOutData);
plt.title("Audio with fade-in and fade-out");
plt.grid()



