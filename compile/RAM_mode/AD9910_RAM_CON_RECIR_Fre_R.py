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

class AD9910_RAM_CON_RECIR_FRE_R(Process):
    """
    write amplitude parameters into AD9910 DRAM
    1024 * 32
    step interval is the time interval betweeen two frequency steps, the unit is (ns)
    """

    def __init__(self, bits, step_interval):
        super().__init__(bits)						

        # get step interval bits for RAM profile register
        high_8_bits, low_8_bits = self.trans_interval(step_interval)

        # RAM profile register 0 data
        CFR1_init_data = [0x80,0x40,0x00,0x00]
        # RAM_PRO0_data = [0x00,0xff,0xff,0xff,0xc0,0x00,0x00,0x04] # 00 01 10 01 00
        RAM_PRO0_data = [0x00,high_8_bits,low_8_bits,0xff,0xc0,0x00,0x00,0x04]

        # write CFR1 process
        write_CFR1_process = Write_Register(self.bits,0x00,CFR1_init_data,4)
        self.instructions += write_CFR1_process.instructions

        # write RAMPRO_0 process
        write_RAMPRO_0_process = Write_Register(self.bits,0x0e,RAM_PRO0_data,8)
        self.instructions += write_RAMPRO_0_process.instructions

        # flip IUP
        flip_IUP_process = Flip_IUP(self.bits)
        self.instructions += flip_IUP_process.instructions

        # legalize
        self.legalize_finish()
        self.legalize_type()

    def trans_interval(self,step_interval,debug=False):
        # assert the step interval is from 4ns to 262140ns
        assert step_interval <= 262140 and step_interval >= 4, f"the step interval {step_interval} is out of the range (4,262140)!"

        # trans the step interval into ratio integer of 4ns
        step_ratio_int = step_interval//4

        # the function for converting to hex number
        def int_to_hex_parts(number):
            # low 8 bits
            low_byte = number & 0xFF
            
            # high 8 bits
            high_byte = (number >> 8) & 0xFF
            
            return high_byte, low_byte

        if debug:
            print(int_to_hex_parts(step_ratio_int))
        
        return int_to_hex_parts(step_ratio_int)
    

if __name__ == "__main__":

    test_AD9910_RAM_CON_RECIR_FRE_R_process = AD9910_RAM_CON_RECIR_FRE_R(len(ALL_SERIAL_PIN),262140)
    a,b = test_AD9910_RAM_CON_RECIR_FRE_R_process.trans_interval(262140,True)
    print(type(a),f"{a:02X}",f"{b:02X}")