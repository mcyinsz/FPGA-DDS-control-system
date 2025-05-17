import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Serial_Programming.pin_mapping import Pin, MRT, CSN, SDI,SCK,IUP,DRC,DRH,PF0,PF1,PF2,OSK, ALL_SERIAL_PIN
from dataclasses import dataclass

class Instruction:
    """
    single instruction
    """

    def __init__(self, instruction_bits:int):
        self.instruction_array = np.zeros(instruction_bits,dtype=int)

        # set all pins invalid
        for pin in ALL_SERIAL_PIN:
            self.clr_pin(pin)

    def keep_last_instruction(self,last_instruction:'Instruction'):
        self.instruction_array = last_instruction.instruction_array
        
    def set_pin(self,pin:Pin):
        self.instruction_array[pin.index]=pin.valid
    
    def clr_pin(self,pin:Pin):
        self.instruction_array[pin.index]=1-pin.valid
    
    def get_instruction_binary_string(self)->str:
        # assert all instruction bits are 0 or 1
        assert all(map(lambda x: x in (0,1),self.instruction_array))

        # generate instruction string
        return ''.join(map(lambda x:str(x), self.instruction_array))
    


if __name__ == "__main__":
    test_Instruction = Instruction(len(ALL_SERIAL_PIN))
    test_Instruction.set_pin(CSN)
    print(test_Instruction.instruction_array)
    print(test_Instruction.get_instruction_binary_string())