import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Serial_Programming.pin_mapping import Pin, MRT, CSN, SDI,SCK,IUP,DRC,DRH,PF0,PF1,PF2,OSK, ALL_SERIAL_PIN
from dataclasses import dataclass
from Serial_Programming.instruction import Instruction
import copy

class Process:

    def __init__(self, bits:int):
        self.bits = bits
        self.instructions = [Instruction(bits)]

    def legalize_type(self):
        """
        each process should satisfy:
        1. it consists a sequence of instructions
        """

        assert all(map(lambda x:isinstance(x,Instruction),self.instructions)), "not all list elements are instructions!"
        
    def legalize_finish(self):
        """
        some processes should satisfy:
        2. their last instruction letting all pins invalid
        """    
        assert all([self.instructions[-1].instruction_array[i]==Instruction(self.bits).instruction_array[i] \
                   for i in range(self.bits)]), "the process does not finish with all pins invalid"
        
    def concatenate(self, following_process:'Process')->None:
        self.instructions = copy.deepcopy(self.instructions) + copy.deepcopy(following_process.instructions)

    def get_instructions(self)->list[str]:
        instructions_string_list = []
        for instruction in self.instructions:
            instructions_string_list.append(instruction.get_instruction_binary_string())
        return instructions_string_list

if __name__ == "__main__":
    test_process = Process(len(ALL_SERIAL_PIN))
    # print(test_process.instructions)
    test_process.concatenate(test_process)
    test_process.legalize_type()
    test_process.legalize_finish()
    print(test_process.get_instructions())
