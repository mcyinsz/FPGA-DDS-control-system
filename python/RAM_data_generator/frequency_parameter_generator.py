import numpy as np
import matplotlib.pyplot as plt

class FrequencyGenerator:
    """
    given a 1024-length frequency ndarray, reshape it for frequency RAM mode
    """

    def __init__(self, Frequency:np.ndarray):
        
        self.original_frequency = self.legalize_clip(Frequency)

        # vectorize convert
        self.frequency = self.original_frequency * 4.294967296
        self.frequency = [int(x) for x in self.frequency]

    def legalize_clip(self,Frequency:np.ndarray):
        # assert length
        assert len(Frequency)==1024, f"the Waveform length {len(Waveform)} is not 1024, which is illegal"

        # convert frequency profile to int type
        Waveform = np.array(np.round(Frequency),dtype=np.int64)

        return Waveform
    
    def visualize_shift(self):
        plt.plot(self.original_frequency*1e-6,"-o")
        plt.xlabel("points")
        plt.ylabel("MHz")
        plt.show()