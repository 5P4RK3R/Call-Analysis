import librosa
import numpy as np
import matplotlib as plt
class DSP:
    def __init__(self) -> None:
        pass

    def snr(self,y) :
        # Calculate SNR
        signal = y  # Assuming entire signal is the desired audio
        noise = np.random.randn(len(y))  # Assuming random noise for demonstration
        snr = 10 * np.log10(np.mean(signal**2) / np.mean(noise**2))
        return snr

    def tempo_beats(y,sr):
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        return tempo, beat_frames

    def load(path):
        y, sr = librosa.load(path=path)
        return y, sr

    def mel_spectogram(y,sr,path):
        fig, ax = plt.subplots()
        s = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)
        S_dB = librosa.power_to_db(s, ref=np.max)
        img = librosa.display.specshow(S_dB, x_axis='time',
                                y_axis='mel', sr=sr,
                                fmax=8000, ax=ax)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')
        plt.savefig(path + 'Mel-frequency spectrogram.png')

    def frequency_power_spectogram(y,sr,path):
        S_full, phase = librosa.magphase(librosa.stft(y))
        idx = slice(*librosa.time_to_frames([10, 15], sr=sr))
        fig, ax = plt.subplots()
        img = librosa.display.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                                y_axis='log', x_axis='time', sr=sr, ax=ax)
        fig.colorbar(img, ax=ax)
        fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
                                    sr=sr, ax=ax[0])
        ax[0].set(title='Linear-frequency power spectrogram')
        ax[0].label_outer()

        hop_length = 1024
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)),
                                    ref=np.max)
        librosa.display.specshow(D, y_axis='log', sr=sr, hop_length=hop_length,
                                x_axis='time', ax=ax[1])
        ax[1].set(title='Log-frequency power spectrogram')
        ax[1].label_outer()
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        plt.savefig(path + 'frequency power spectrogram.png')

    def formant(y,sr):
        # Extract formants using LPC analysis (example, actual method may vary)
        order = 12  # LPC order
        lpc_coeffs = librosa.lpc(y, order=order)
        roots = np.roots(lpc_coeffs)
        formants_hz = np.sort(np.abs(np.angle(roots) * (sr / (2 * np.pi))))

        # Compute KPIs
        f1_hz = formants_hz[0]
        f2_hz = formants_hz[1]
        f3_hz = formants_hz[2]
        f2_f1_ratio = f2_hz / f1_hz
        # Compute other KPIs as needed...

        # Print KPIs
        print("F1 Frequency:", f1_hz, "Hz")
        print("F2 Frequency:", f2_hz, "Hz")
        print("F3 Frequency:", f3_hz, "Hz")
        print("F2/F1 Ratio:", f2_f1_ratio)
        return  f2_f1_ratio

    def waveplot(y,sr):
        librosa.display.waveplot(y, sr=sr)