import numpy as np
from ICache.I_Cache_generator import ICacheGenerator
import RAM_mode.AD9910_RAM_CON_RECIR_Fre_R
import RAM_mode.AD9910_RAM_init
import RAM_mode.AD9910_WAVE_RAM_FRE_W

from Serial_Programming.AD9910_init import Process,AD9910_init
from Serial_Programming.pin_mapping import ALL_SERIAL_PIN
from Serial_Programming.AD9910_Single_tone import SingleToneInit,SingleToneSet
import RAM_mode
from RAM_data_generator.frequency_parameter_generator import FrequencyGenerator

import os

# change this for different frequency patterns
frequency_performance = np.repeat(np.linspace(55e6,105e6,128),8)

# change frequency step interval for different intervals
frequency_step_interval = 8000 # ns

# file name
dir_name = os.path.join(os.path.dirname(os.path.dirname(__file__)),"temp")
coe_file_name = "test_file.coe"

test_generator = FrequencyGenerator(frequency_performance)
test_generator.visualize_shift()


bits =len(ALL_SERIAL_PIN)
test_AD9910_init = AD9910_init(bits)
test_AD9910_RAM_init = RAM_mode.AD9910_RAM_init.AD9910_RAM_init(bits)


test_AD9910_WAVE_Fre_W = RAM_mode.AD9910_WAVE_RAM_FRE_W.AD9910_WAVE_RAM_FRE_W(bits,test_generator.frequency)
test_AD9910_RAM_CON_RECIR_Fre_R = RAM_mode.AD9910_RAM_CON_RECIR_Fre_R.AD9910_RAM_CON_RECIR_FRE_R(bits,frequency_step_interval)

this_process = Process(len(ALL_SERIAL_PIN))

this_process.concatenate(test_AD9910_init)
this_process.concatenate(test_AD9910_RAM_init)
this_process.concatenate(test_AD9910_WAVE_Fre_W)
this_process.concatenate(test_AD9910_RAM_CON_RECIR_Fre_R)


test_i_cache_generator = ICacheGenerator(this_process)

# change file name here
test_i_cache_generator.write_coe_file(os.path.join(dir_name,coe_file_name))