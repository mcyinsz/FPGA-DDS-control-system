import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from compile import ICacheGenerator,Process,AD9910_init,SingleToneInit,SingleToneSet,ALL_SERIAL_PIN

def generate_singletone_coe(
    frequency: int, # Hz
    amplitude: int, # binary
    phase: int, # degree
    target_path: str, # .coe path
    channel: int = 0 # 0-7
):
    test_AD9910_init = AD9910_init(len(ALL_SERIAL_PIN))

    test_Single_Tone_init = SingleToneInit(len(ALL_SERIAL_PIN))
    test_Single_Tone_set = SingleToneSet(len(ALL_SERIAL_PIN),channel,frequency,amplitude,phase)

    this_process = Process(len(ALL_SERIAL_PIN))
    this_process.concatenate(test_AD9910_init)
    this_process.concatenate(test_Single_Tone_init)
    this_process.concatenate(test_Single_Tone_set)
    print(len(this_process.get_instructions()))

    test_i_cache_generator = ICacheGenerator(this_process)
    test_i_cache_generator.write_coe_file(target_path)

if __name__ == "__main__":

    # parameters
    frequency = 445 * 1e6
    amplitude = 10239
    phase = 0

    # file name
    dir_name = os.path.join(os.path.dirname(os.path.dirname(__file__)),"temp")
    coe_file_name = "singletone_routine_test.coe"
    target_path = os.path.join(dir_name,coe_file_name)

    generate_singletone_coe(frequency,amplitude,phase,target_path)