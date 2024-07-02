import librosa
import numpy as np
import matplotlib.pyplot as plt

def main():
  y, sr = librosa.load('Gravity Falls.wav', duration=40)
  librosa.feature.chroma_stft(y=y, sr=sr)
  print("Sampling Rate: ", sr)
  S = np.abs(librosa.stft(y, n_fft=4096))**2
  chroma = librosa.feature.chroma_stft(S=S, sr=sr)
  print(chroma)
  print(chroma.shape)
  max_pitch_profile = -1
  pitch_changs = 0
  highest_pitches = []
  for i in range(chroma.shape[1]):
    pitches = []
    for j in range(chroma.shape[0]):
        pitches.append((j, chroma[j][i]))

    #pitches[*][0] is the key, pitches[*][1] is the value
    pitches.sort(key=lambda x: x[1], reverse=True)
    max_pitches = [p[0] for p in pitches if p[1] == 1]
    if max_pitch_profile in max_pitches:
      continue
    # Find all pitches with energy equal to 1
    # if pitches[0][0] != max_pitch_profile and pitches[0][1] > 0.5:
    #     max_pitch_profile = pitches[0][0]
    #     print("Time: ", i, " Pitch: ", pitches[0][0], " Energy: ", pitches[0][1])
    #     pitch_changs += 1
    highest_pitches.append(pitches[0][0])
  i = 0
  while i < len(highest_pitches) - 1:
    if i == 0 and highest_pitches[i] != highest_pitches[i + 1]:
      highest_pitches.pop(i)
    elif i == len(highest_pitches) - 1 and highest_pitches[i] != highest_pitches[i - 1]:
      highest_pitches.pop(i)
    elif highest_pitches[i] != highest_pitches[i - 1] and highest_pitches[i] != highest_pitches[i + 1]:
      highest_pitches.pop(i)
    else:
      i += 1
  print(highest_pitches, "\n")


  # print("Pitch Changes: ", pitch_changs)
  print(highest_pitches)
    
  fig, ax = plt.subplots(nrows=2, sharex=False)
  # img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
  # fig.colorbar(img, ax=[ax[0]])
  # ax[0].label_outer()
  img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[0])
  fig.colorbar(img, ax=ax)
  # graph highest_pitches
  ax[1].plot(highest_pitches)
  ax[1].set_title('Highest Pitch')
  ax[1].label_outer()
  plt.show()

if __name__ == "__main__":
    main() 