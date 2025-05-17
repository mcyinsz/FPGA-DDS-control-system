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


class AD9910_init(Process):

    def __init__(self, bits):
        """
        reset AD9910 and set CFR3 & Assistant Register
        """
        super().__init__(bits)

        # reset AD9910 by flip AD9910 MRT
        reset_instruction_1 = Instruction(bits)
        reset_instruction_1.set_pin(MRT)
        self.instructions.append(reset_instruction_1)

        reset_instruction_2 = Instruction(bits)
        self.instructions.append(reset_instruction_2)

        # set CSN valid
        CSN_valid_instruction = Instruction(bits)
        CSN_valid_instruction.set_pin(CSN)
        self.instructions.append(CSN_valid_instruction)

        # write CFR3 register
        write_CFR3_register_address_process = Write_8_bit(bits,data=0x02)
        self.instructions += write_CFR3_register_address_process.instructions

        # set CFR3 data
        CFR3_init_data=[0x05,0x0F,0x41,0x50]
        for data in CFR3_init_data:
            tmp_write_8_bit_process = Write_8_bit(bits,data)
            self.instructions += tmp_write_8_bit_process.instructions
        
        # set CSN invalid
        CSN_invalid_instruction = Instruction(bits)
        self.instructions.append(CSN_invalid_instruction)

        # set CSN valid
        CSN_valid_instruction = Instruction(bits)
        CSN_valid_instruction.set_pin(CSN)
        self.instructions.append(CSN_valid_instruction)

        # write assistant register
        write_ASS_register_address_process = Write_8_bit(bits,data=0x03)
        self.instructions += write_ASS_register_address_process.instructions

        # set ASS data
        ASS_init_data=[0x00,0x00,0x00,0x7F]
        for data in ASS_init_data:
            tmp_write_8_bit_process = Write_8_bit(bits,data)
            self.instructions += tmp_write_8_bit_process.instructions

        # set CSN invalid
        CSN_invalid_instruction = Instruction(bits)
        self.instructions.append(CSN_invalid_instruction)
        
        # flip IUP
        IUP_flip_instruction_1 = Instruction(bits)
        IUP_flip_instruction_1.set_pin(IUP)
        self.instructions.append(IUP_flip_instruction_1)
        IUP_flip_instruction_2 = Instruction(bits)
        self.instructions.append(IUP_flip_instruction_2)

        # legalize
        self.legalize_type()
        self.legalize_finish()

if __name__ == "__main__":
    test_AD9910_init = AD9910_init(len(ALL_SERIAL_PIN))
    print(test_AD9910_init.get_instructions())

