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
from Serial_Programming.high_level_serial_programming import Write_Register,Flip_IUP,Write_RAM

class AD9910_WAVE_RAM_FRE_W(Process):
    """
    write amplitude parameters into AD9910 DRAM
    1024 * 32
    """

    def __init__(self, bits, RAM_FRE:list[int]):
        super().__init__(bits)								

        # RAM profile register 0 data
        CFR1_init_data = [0x00,0x40,0x00,0x00]
        RAM_PRO0_data = [0x00,0xff,0xff,0xff,0xC0,0x00,0x00,0x00]
        CFR2_init_data=[0x00,0x40,0x08,0x20]

        # write CFR1 process
        write_CFR1_process = Write_Register(self.bits,0x00,CFR1_init_data,4)
        self.instructions += write_CFR1_process.instructions

        # write CFR2 process
        write_CFR2_process = Write_Register(self.bits,0x01,CFR2_init_data,4)
        self.instructions += write_CFR2_process.instructions

        # write RAMPRO_0 process
        write_RAMPRO_0_process = Write_Register(self.bits,0x0e,RAM_PRO0_data,8)
        self.instructions += write_RAMPRO_0_process.instructions

        # flip IUP
        flip_IUP_process = Flip_IUP(self.bits)
        self.instructions += flip_IUP_process.instructions

        # write RAM process
        write_RAM_process = Write_RAM(self.bits,RAM_data=RAM_FRE)
        self.instructions += write_RAM_process.instructions

        # flip IUP
        flip_IUP_process = Flip_IUP(self.bits)
        self.instructions += flip_IUP_process.instructions

        # legalize
        self.legalize_finish()
        self.legalize_type()


