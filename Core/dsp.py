import numpy as np

class DSP:
    def __init__(self) -> None:
        pass

    def snr(self,y) -> None:
        # Calculate SNR
        signal = y  # Assuming entire signal is the desired audio
        noise = np.random.randn(len(y))  # Assuming random noise for demonstration
        snr = 10 * np.log10(np.mean(signal**2) / np.mean(noise**2))
