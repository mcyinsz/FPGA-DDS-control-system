import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dataclasses import dataclass

"""
For AD9910 Serial programming, we should control at least following pins:
    MRT: reset AD9910
    CSN: chip selection bit (low valid)
    SCK: sychronized serial data passing clock
    SDI: serial Data input
    IUP: for update the state of AD9910
    PF0-PF2: profile index pins
    OSK: output shift keying pin for modifying amplitude
    DRH: digital harmonics hold
    DRC: digital harmonics control 
we should first determine the relation between verilog I-Cache pins and AD9910 pins
"""

@dataclass
class Pin:
    index: int
    valid: int

# 定义每个引脚
MRT = Pin(index=0, valid=1)
CSN = Pin(index=1, valid=0)
SCK = Pin(index=2, valid=1)
SDI = Pin(index=3, valid=1)
IUP = Pin(index=4, valid=1)
PF0 = Pin(index=5, valid=1)
PF1 = Pin(index=6, valid=1)
PF2 = Pin(index=7, valid=1)
OSK = Pin(index=8, valid=1)
DRH = Pin(index=9, valid=1)
DRC = Pin(index=10, valid=1)

ALL_SERIAL_PIN = (MRT,CSN, SDI,SCK,IUP,DRC,DRH,PF0,PF1,PF2,OSK)

if __name__ == "__main__":
    print(MRT.index)
    print(1-CSN.valid)
    print(SCK)
    print(SDI)
    print(IUP)
    print(PF0)
    print(PF1)
    print(PF2)
    print(OSK)