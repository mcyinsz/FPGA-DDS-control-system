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

class Write_Register(Process):
    """
    complete Write Register process including CSN instructions, address instructions and data instructions
    """
    def __init__(self, bits, reg_address:int, reg_data:list[int], element_number:int):
        super().__init__(bits)
        self.instructions = []
        self.legalize_address(reg_address)
        self.legalize_data(reg_data,element_number)
        self.reg_address = reg_address
        self.reg_data = reg_data

        # set CSN valid
        CSN_valid_instruction = Instruction(bits)
        CSN_valid_instruction.set_pin(CSN)
        self.instructions.append(CSN_valid_instruction)

        # write register address
        write_register_address_process = Write_8_bit(bits,data=self.reg_address)
        self.instructions += write_register_address_process.instructions

        # set register data
        for data in self.reg_data:
            tmp_write_8_bit_process = Write_8_bit(bits,data)
            self.instructions += tmp_write_8_bit_process.instructions

        # set CSN invalid
        CSN_invalid_instruction = Instruction(bits)
        self.instructions.append(CSN_invalid_instruction)

        # valify length of instructions
        assert len(self.instructions) == 2+(8+element_number*8)*2
        self.legalize_type()
        self.legalize_finish()

    def legalize_address(self,address):
        assert isinstance(address,int), f"illegal address type {type(address)}"
        assert address >= 0x00 and address<= 0x15, f"address out of range {address}"

    def legalize_data(self,reg_data:list[int],element_number):
        assert all(map(lambda x:isinstance(x,int),reg_data)), f"illegal data type"
        assert len(reg_data)==element_number, f"data element number {len(reg_data)} is not equal to element number {element_number}"
    
    
class Flip_IUP(Process):

    """
    flip IUP signal to update the output of AD9910
    """

    def __init__(self, bits):
        super().__init__(bits)
        # reload self instructions
        self.instructions = []
        # flip IUP
        IUP_flip_instruction_1 = Instruction(bits)
        IUP_flip_instruction_1.set_pin(IUP)
        self.instructions.append(IUP_flip_instruction_1)
        IUP_flip_instruction_2 = Instruction(bits)
        self.instructions.append(IUP_flip_instruction_2)

        # legalize
        assert len(self.instructions) == 2
        self.legalize_type()
        self.legalize_finish()

class Write_RAM(Process):

    def __init__(self, bits, RAM_data:list[int]):
        super().__init__(bits)

        # reload self.instruction
        self.instructions = []

        # set CSN valid
        CSN_valid_instruction = Instruction(bits)
        CSN_valid_instruction.set_pin(CSN)
        self.instructions.append(CSN_valid_instruction)

        # legalize RAM_data
        self.legalize_data(RAM_data)

        # write register address
        write_register_address_process = Write_8_bit(bits,data=0x16)
        self.instructions += write_register_address_process.instructions

        # set register data
        for data in RAM_data:
            tmp_write_8_bit_process = Write_32_bit(bits,data)
            self.instructions += tmp_write_8_bit_process.instructions

        # set CSN invalid
        CSN_invalid_instruction = Instruction(bits)
        self.instructions.append(CSN_invalid_instruction)

        # legalize length:  2 CSN instructions + 8*2 address instructions + 32*2*1024 RAM instructions
        assert len(self.instructions) == 2+8*2+32*2*1024
        self.legalize_type()
        self.legalize_finish()


    def legalize_data(self,RAM_data):
        assert len(RAM_data) == 1024, f"the RAM data length is illegal {len(RAM_data)}"
        assert all(map(lambda x:isinstance(x,int),RAM_data)), f"existing RAM data with not-integer type"
        


if __name__ == "__main__":
    test_Write_register = Write_Register(len(ALL_SERIAL_PIN),0x02,[0x05,0x0F,0x41,0x50],4)
    print(test_Write_register.get_instructions())

    test_flip_IUP = Flip_IUP(len(ALL_SERIAL_PIN))
    print(test_flip_IUP.get_instructions())