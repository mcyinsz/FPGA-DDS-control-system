import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Serial_Programming.pin_mapping import Pin, MRT, CSN, SDI,SCK,IUP,DRC,DRH,PF0,PF1,PF2,OSK, ALL_SERIAL_PIN
from dataclasses import dataclass
from Serial_Programming.instruction import Instruction
from Serial_Programming.abstract_process import Process
import copy
from Serial_Programming.write_bit_process import Write_32_bit,Write_8_bit
from Serial_Programming.high_level_serial_programming import Write_Register,Flip_IUP

class AD9910_RAM_CW_Fre_Set(Process):
    """
    set carry wave frequency
    """

    def __init__(self, bits, frequency:float):
        super().__init__(bits)

        # prepare FTW register (frequency register) value
        FTW_value_list = [0x00,0x00,0xa7,0xc6]

        # get converted integer frequency value
        self.frequency = self.frequency_convert(frequency)

        # update FTW value
        FTW_value_list[3] = self.frequency & 0xFF
        FTW_value_list[2] = (self.frequency >> 8) & 0xFF
        FTW_value_list[1] = (self.frequency >> 16) & 0xFF
        FTW_value_list[0] = (self.frequency >> 24) & 0xFF

        # write register process
        write_FTW_process = Write_Register(self.bits,0x07,FTW_value_list,4)
        self.instructions += write_FTW_process.instructions

        # flip IUP
        flip_IUP_process = Flip_IUP(self.bits)
        self.instructions += flip_IUP_process.instructions

    def frequency_convert(self,frequency:float)->int:
        assert frequency>=0 and frequency<=450*1e6, f"frequency {frequency} out of range 0Hz - 450MHz"
        return int(frequency * 4.294967296)
    

if __name__ == "__main__":
    test_RAM_CW_Fre_init = AD9910_RAM_CW_Fre_init(len(ALL_SERIAL_PIN),1e6)
    assert len(test_RAM_CW_Fre_init.instructions) == 85
    print(test_RAM_CW_Fre_init.get_instructions())
    print(test_RAM_CW_Fre_init.frequency)