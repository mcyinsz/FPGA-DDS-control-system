import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from compile import AD9910_init,AD9910_RAM_init,AD9910_WAVE_RAM_FRE_W,\
    AD9910_RAM_CON_RECIR_FRE_R,ALL_SERIAL_PIN,FrequencyGenerator,Process, ICacheGenerator

import os

def generate_frequency_shift_coe(
    frequency_performance: np.ndarray, # frequency array (Hz)
    frequency_step_interval: int, # ns
    target_path: str, # .coe file path
    visualize: bool = False # visualize the setup frequency waveform
):
    test_generator = FrequencyGenerator(frequency_performance)
    
    if visualize:
        test_generator.visualize_shift()

    bits = len(ALL_SERIAL_PIN)
    test_AD9910_init = AD9910_init(bits)
    test_AD9910_RAM_init = AD9910_RAM_init(bits)


    test_AD9910_WAVE_Fre_W = AD9910_WAVE_RAM_FRE_W(bits,test_generator.frequency)
    test_AD9910_RAM_CON_RECIR_Fre_R = AD9910_RAM_CON_RECIR_FRE_R(bits,frequency_step_interval)

    this_process = Process(len(ALL_SERIAL_PIN))

    this_process.concatenate(test_AD9910_init)
    this_process.concatenate(test_AD9910_RAM_init)
    this_process.concatenate(test_AD9910_WAVE_Fre_W)
    this_process.concatenate(test_AD9910_RAM_CON_RECIR_Fre_R)


    test_i_cache_generator = ICacheGenerator(this_process)

    # change file name here
    test_i_cache_generator.write_coe_file(target_path)

if __name__ == "__main__":

    # change this for different frequency patterns
    frequency_performance = np.repeat(np.linspace(55e6,105e6,128),8)

    # change frequency step interval for different intervals
    frequency_step_interval = 8000 # ns

    # file name
    dir_name = os.path.join(os.path.dirname(os.path.dirname(__file__)),"temp")
    coe_file_name = "frequency_shift_routine_test.coe"
    target_path = os.path.join(dir_name,coe_file_name)

    generate_frequency_shift_coe(
        frequency_performance=frequency_performance,
        frequency_step_interval=frequency_step_interval,
        target_path=target_path,
        visualize=False
    )