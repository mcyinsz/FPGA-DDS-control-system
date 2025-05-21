import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Serial_Programming.abstract_process import Process



class ICacheGenerator():
    """
    like abstract ROM, I-Cache can be considered as a ROM, with pre-determined width and control bits
    """

    def __init__(self,Process:Process)->None:
        """
        initialize a I-Cache generator object with a Processes list
        """
        self.process = Process
        self.length = len(Process.get_instructions())

    def _legalize(self):
        assert isinstance(self.process,Process), f"invalid type {type(self.process)}, input must be process"
    
    def write_coe_file(self,file_path:str):
        with open(file_path,"w") as file:
            file.write("memory_initialization_radix=2;\n")
            file.write("memory_initialization_vector=\n")
            for i,instruction in enumerate(self.process.get_instructions()):
                print(f"write: {i}, {instruction[::-1]}")
                if i!=self.length-1:
                    file.write(instruction[::-1] + ",\n")
                else:
                    file.write(instruction[::-1] + ";")


