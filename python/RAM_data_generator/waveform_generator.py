import numpy as np

class WaveformGenerator:
    """
    given a 1024-length waveform ndarray, reshape it for polarity RAM mode
    """

    def __init__(self, Waveform:np.ndarray):
        
        self.waveform = self.legalize_clip(Waveform)

        # vectorize convert
        vectorize_convert = np.vectorize(self.convert_polarity)
        self.waveform = vectorize_convert(self.waveform)
        self.waveform = [int(x) for x in self.waveform]

    def legalize_clip(self,Waveform:np.ndarray):
        # assert length
        assert len(Waveform)==1024, f"the Waveform length {len(Waveform)} is not 1024, which is illegal"

        # 14-bit amplitude range
        max_value = np.max(Waveform)
        min_value = abs(np.min(Waveform))

        # scale the waveform
        max_abs = max(max_value,min_value)
        reference = 2**14 - 1
        Waveform = Waveform * (reference/max_abs) 

        # convert waveform to int type
        Waveform = np.array(np.round(Waveform),dtype=np.int64)

        return Waveform

    def convert_phase(self,waveform_element:int):
        # the phase is completely determined by the symbol
        phase =  0x00000000 if waveform_element>=0 else 0x7fff0000
        return phase


    def convert_amplitude(self,waveform_element:int):
        # 14 bit amplitude word
        waveform_element = np.abs(waveform_element)
        amplitude = waveform_element<<2
        return amplitude
    
    def convert_polarity(self,waveform_element:int):
        # 30 bit polarity word
        return self.convert_amplitude(waveform_element)+self.convert_phase(waveform_element)
    

if __name__ == "__main__":


    test_sine = np.sin(np.linspace(0,2*np.pi,1024))*100
    test_waveformgenerator = WaveformGenerator(test_sine)
    test_waveformgenerator.legalize_clip(test_sine)
    print(test_waveformgenerator.waveform)
    
