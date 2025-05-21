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

class Write_single_bit(Process):
    """
    write single bit in AD9910 include two instructions:
    1. change SDI bit
    2. Flip SCK bit 
    """

    def __init__(self, bits:int, data:int):
        super().__init__(bits)
        
        # data should be in 0,1
        assert data in (0,1), "invalid data"
        
        self.first_instruction = Instruction(bits)
        self.first_instruction.set_pin(CSN)
        if data:
            self.first_instruction.set_pin(SDI)
        
        self.second_instruction = copy.deepcopy(self.first_instruction)
        self.second_instruction.set_pin(SCK)

        self.instructions = [self.first_instruction, self.second_instruction]
        self.legalize_type()

class Write_8_bit(Process):
    """
    write 8 bit in AD9910 includes 8 write 1 bit instructions
    """

    def __init__(self, bits:int, data:int):
        """
        bits: instruction width 
        data: an unsigned 8 bit integer 0-255
        """
        super().__init__(bits)

        self.data_list = self.convert_to_binary_list(data)

        self.instructions = []

        # 8 write 1 bit instructions process
        for i in range(8):
            self.instructions+=Write_single_bit(bits,self.data_list[i]).instructions
        

    def convert_to_binary_list(self,data:int):
        """
        input an integer, output a bit list in the MSB -> LSB order
        """
        assert isinstance(data,int), f"the data type {type(data)} is not valid"
        assert data<=255 and data>=0, f"the data {data} is out of range"

        mask = 0x80
        binary_list = []
        for i in range(8):
            if mask>>i & data:
                binary_list.append(1)
            else:
                binary_list.append(0)
        return binary_list

class Write_32_bit(Process):
    """
    write 32 bit in AD9910 includes 32 write 1 bit instructions
    """

    def __init__(self, bits:int, data:int):
        """
        bits: instruction width 
        data: an unsigned 8 bit integer 0-255
        """
        super().__init__(bits)

        self.data_list = self.convert_to_binary_list(data)

        self.instructions = []

        # 8 write 1 bit instructions process
        for i in range(32):
            self.instructions+=Write_single_bit(bits,self.data_list[i]).instructions
        

    def convert_to_binary_list(self,data:int):
        """
        input an integer, output a bit list in the MSB -> LSB order
        """
        assert isinstance(data,int), f"the data type {type(data)} is not valid"
        assert data<=0xffffffff and data>=0, f"the data {data} is out of range"

        mask = 0x80000000
        binary_list = []
        for i in range(32):
            if mask>>i & data:
                binary_list.append(1)
            else:
                binary_list.append(0)
        return binary_list

if __name__ == "__main__":
    test_write_single_bit = Write_single_bit(len(ALL_SERIAL_PIN),1)
    print(test_write_single_bit.get_instructions())
    
    test_write_8_bit = Write_8_bit(len(ALL_SERIAL_PIN),27)
    print(test_write_8_bit.data_list)
    print(test_write_8_bit.get_instructions())

    test_write_32_bit = Write_32_bit(len(ALL_SERIAL_PIN),27)
    print(test_write_32_bit.data_list)
    print(len(test_write_32_bit.get_instructions()))