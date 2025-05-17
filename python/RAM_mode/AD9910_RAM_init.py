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


class AD9910_RAM_init(Process):

    def __init__(self, bits):
        """
        set AD9910 as RAM mode and set CFR2 & RAMPROfile Register
        """
        super().__init__(bits)

        # prepare register values
        CFR1_init_data = [0x00,0x40,0x00,0x00]
        CFR2_init_data = [0x01,0x40,0x08,0x20]
        RAMprofile_init_data = [0x3f, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        # write CFR1 process
        write_CFR1_process = Write_Register(self.bits,0x00,CFR1_init_data,4)
        self.instructions += write_CFR1_process.instructions

        # write CFR2 process
        write_CFR2_process = Write_Register(self.bits,0x01,CFR2_init_data,4)
        self.instructions += write_CFR2_process.instructions

        # write RAMPRO_0 process
        write_RAMPRO_process = Write_Register(self.bits,0x0e,RAMprofile_init_data,8)
        self.instructions += write_RAMPRO_process.instructions
        
        # flip IUP
        IUP_flip_process = Flip_IUP(self.bits)
        self.instructions += IUP_flip_process.instructions

        # legalize
        self.legalize_type()
        self.legalize_finish()


if __name__ == "__main__":
    test_AD9910_RAM_init = AD9910_RAM_init(len(ALL_SERIAL_PIN))
    print(len(test_AD9910_RAM_init.get_instructions()))
    assert len(test_AD9910_RAM_init.instructions)==313, "someting wrong for AD9910 RAM init class"
    # 1 init instruction + 2 * [(32+8)*2] write register instructions + (64+8)*2 write register instructions + 2*3 CSN instructions + 2 flip IUP instructions = 313 instructions

    print(test_AD9910_RAM_init.get_instructions())