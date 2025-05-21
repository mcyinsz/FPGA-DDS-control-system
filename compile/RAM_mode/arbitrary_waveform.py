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