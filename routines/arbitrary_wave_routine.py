import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from compile import ICacheGenerator,Process,AD9910_init,AD9910_RAM_init,AD9910_RAM_CW_Fre_Set,AD9910_RAM_CW_Fre_init,AD9910_WAVE_RAM_AMP_W,AD9910_RAM_CON_RECIR_AMP_R,ALL_SERIAL_PIN,WaveformGenerator
import numpy as np

def generate_arbitrary_wave_coe(
    waveform_array: np.ndarray, # waveform amplitude sample points
    target_path: str, # .coe result path
    carry_wave_frequency: int = 0 # carry wave frequency (Hz)
):

    waveform = WaveformGenerator(waveform_array)
    bits =len(ALL_SERIAL_PIN)
    test_AD9910_init = AD9910_init(bits)
    test_AD9910_RAM_init = AD9910_RAM_init(bits)
    test_RAM_CW_Fre_init = AD9910_RAM_CW_Fre_init(bits)
    test_RAM_CW_Fre_set = AD9910_RAM_CW_Fre_Set(bits,carry_wave_frequency)
    test_AD9910_WAVE_RAM_W = AD9910_WAVE_RAM_AMP_W(bits,waveform.waveform)
    test_AD9910_RAM_CON_RECIR_AMP_R = AD9910_RAM_CON_RECIR_AMP_R(bits)

    this_process = Process(len(ALL_SERIAL_PIN))

    this_process.concatenate(test_AD9910_init)
    this_process.concatenate(test_AD9910_RAM_init)
    this_process.concatenate(test_RAM_CW_Fre_init)
    this_process.concatenate(test_RAM_CW_Fre_set)
    this_process.concatenate(test_AD9910_WAVE_RAM_W)
    this_process.concatenate(test_AD9910_RAM_CON_RECIR_AMP_R)


    test_i_cache_generator = ICacheGenerator(this_process)
    test_i_cache_generator.write_coe_file(target_path)

if __name__ == "__main__":
    
    # arbitrary tanh waveform
    x = np.linspace(0,np.pi,1024)
    y = np.tan(x)
    
    # plot and show
    import matplotlib.pyplot as plt
    plt.plot(x,y)
    plt.show()

    # file name
    dir_name = os.path.join(os.path.dirname(os.path.dirname(__file__)),"temp")
    coe_file_name = "arbitrary_wave_routine_test.coe"
    target_path = os.path.join(dir_name,coe_file_name)

    # generate .coe
    generate_arbitrary_wave_coe(
        waveform_array=y,
        target_path=target_path
    )