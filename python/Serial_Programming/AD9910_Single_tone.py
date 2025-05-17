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

class SingleToneInit(Process):

    def __init__(self, bits):
        """
        initialize Single Tone mode
        """
        super().__init__(bits)

        # set CSN valid
        CSN_valid_instruction = Instruction(bits)
        CSN_valid_instruction.set_pin(CSN)
        self.instructions.append(CSN_valid_instruction)

        # write CFR1 register
        write_CFR1_register_address_process = Write_8_bit(bits,data=0x00)
        self.instructions += write_CFR1_register_address_process.instructions

        # set CFR1 data
        CFR1_init_data=[0x00,0x40,0x00,0x00]
        for data in CFR1_init_data:
            tmp_write_8_bit_process = Write_8_bit(bits,data)
            self.instructions += tmp_write_8_bit_process.instructions
        
        # set CSN invalid
        CSN_invalid_instruction = Instruction(bits)
        self.instructions.append(CSN_invalid_instruction)

        # set CSN valid
        CSN_valid_instruction = Instruction(bits)
        CSN_valid_instruction.set_pin(CSN)
        self.instructions.append(CSN_valid_instruction)

        # write CFR2 register
        write_CFR2_register_address_process = Write_8_bit(bits,data=0x01)
        self.instructions += write_CFR2_register_address_process.instructions

        # set CFR1 data
        CFR2_init_data=[0x01,0x40,0x08,0x20]
        for data in CFR2_init_data:
            tmp_write_8_bit_process = Write_8_bit(bits,data)
            self.instructions += tmp_write_8_bit_process.instructions
        
        # set CSN invalid
        CSN_invalid_instruction = Instruction(bits)
        self.instructions.append(CSN_invalid_instruction)

        # flip IUP
        # TODO: 这里有一个隐患，就是在片选信号置为无效之后立刻翻转了IUP
        IUP_flip_instruction_1 = Instruction(bits)
        IUP_flip_instruction_1.set_pin(IUP)
        self.instructions.append(IUP_flip_instruction_1)
        IUP_flip_instruction_2 = Instruction(bits)
        self.instructions.append(IUP_flip_instruction_2)

        # legalize
        self.legalize_type()
        self.legalize_finish()


class SingleToneSet(Process):

    def __init__(self, 
                 bits:int, 
                 profile:int, 
                 frequency:float, 
                 amplitude:int,
                 phase:float
                 ):
        """
        set one single tone profile
        frequency: 1 Hz ~ 450 MHz
        phase: 0~360°
        amplitude: 0x0000--0x3FFF
        """
        super().__init__(bits)

        # convert AD9910 DDS parameters
        self.frequency = self.frequency_convert(frequency)
        self.amplitude = self.amplitude_convert(amplitude)
        self.phase = self.phase_convert(phase)

        # get profile register address and data
        self.address = self.get_profile_address(profile)
        self.data = self.get_profile_data()

        # set CSN valid
        CSN_valid_instruction = Instruction(bits)
        CSN_valid_instruction.set_pin(CSN)
        self.instructions.append(CSN_valid_instruction)

        # write profile register
        write_profile_register_address_process = Write_8_bit(bits,data=self.address)
        self.instructions += write_profile_register_address_process.instructions

        # set profile data
        for i in range(8):
            tmp_write_8_bit_process = Write_8_bit(bits,self.data[i])
            self.instructions += tmp_write_8_bit_process.instructions
        
        # set CSN invalid
        CSN_invalid_instruction = Instruction(bits)
        self.instructions.append(CSN_invalid_instruction)

        # flip IUP
        # TODO: 这里有一个隐患，就是在片选信号置为无效之后立刻翻转了IUP
        IUP_flip_instruction_1 = Instruction(bits)
        IUP_flip_instruction_1.set_pin(IUP)
        self.instructions.append(IUP_flip_instruction_1)
        IUP_flip_instruction_2 = Instruction(bits)
        self.instructions.append(IUP_flip_instruction_2)

        # legalize
        self.legalize_type()
        self.legalize_finish()




    
    def frequency_convert(self,frequency:float)->int:
        assert frequency>=1 and frequency<=450*1e6, f"frequency {frequency} out of range 1Hz - 450MHz"
        return int(frequency * 4.294967296)
    
    def phase_convert(self,phase:float)->int:
        assert phase>=0 and phase<=360, f"phase {phase} out of range 0 - 360 degrees"
        return int(phase*182.044444444)

    def amplitude_convert(self,amplitude:int)->int:
        assert isinstance(amplitude,int), f"amplitude should be int type, input {type(amplitude)} type"
        assert amplitude>=0 and amplitude<=0x3FFF, f"amplitude {amplitude} out of range 0x0000 - 0x3FFF"
        return amplitude
    
    def get_profile_address(self,profile:int)->int:
        assert profile in [0,1,2,3,4,5,6,7], f"invalid profile number {profile}, profile number should be in 0-7"
        register_address_list = [0x0e,0x0f,0x10,0x11,0x12,0x13,0x14,0x15]
        return register_address_list[profile]

    def get_profile_data(self)->list:
        Profile_All = [0] * 8
        Profile_All[7] = self.frequency & 0xFF
        Profile_All[6] = (self.frequency >> 8) & 0xFF
        Profile_All[5] = (self.frequency >> 16) & 0xFF
        Profile_All[4] = (self.frequency >> 24) & 0xFF
        Profile_All[3] = self.phase & 0xFF
        Profile_All[2] = (self.phase >> 8) & 0xFF
        Profile_All[1] = self.amplitude & 0xFF
        Profile_All[0] = (self.amplitude >> 8) & 0xFF
        return Profile_All



if __name__ == "__main__": 
    test_Single_Tone_init = SingleToneInit(len(ALL_SERIAL_PIN))
    print(test_Single_Tone_init.get_instructions())

    test_Single_Tone_set = SingleToneSet(len(ALL_SERIAL_PIN),0,450*1e6,0x3FFF,360)
    print(test_Single_Tone_set.get_instructions())
    print(test_Single_Tone_set.get_profile_data())