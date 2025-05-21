# FPGA - DDS control system

A control system designed for signal generating. Support AD9910 DDS Chip.

## system overview

* Hardware architecture tree: Server - FPGA - DDS(AD9910)
* Software Organization: Instruction compile System (implemented with `Python`) & On-chip hardware logic (implemented with `Verilog`)

![alt text](/pics/system_overview.png)

## routines (instruction flows)

* SingleTone Routine

``` python
generate_singletone_coe(
    frequency, # frequency with unit Hz
    amplitude, # binary amplitude, max 0x3FFF
    phase, # initial phase with unit degree 0 - 360
    target_path, # .coe path
    channel # 0-7, AD9910 singletone channel
)
```

* Arbitrary Wave Routine

``` python
generate_arbitrary_wave_coe(
    waveform_array, # waveform amplitude sample points (1024 elements)
    target_path, # .coe result path
    carry_wave_frequency # carry wave frequency (Hz)
)
```

* Frequency Shift Routine

``` python
generate_frequency_shift_coe(
    frequency_performance, # frequency sample points (Hz, 1024 elements)
    frequency_step_interval, # the time interval between two neighboring frequency points (ns)
    target_path, # .coe file path
    visualize# visualize the setup frequency waveform
)
```

## FPGA logic unit

### instruction counter

Each instruction counter is a hardware module, which is able to output instructions with given data width one-by-one.

The instruction counter also consists a clock divider, for satisfying timing constraints.

The instruction counter's output is a bus indicating the current instruction address, for addressing the FPGA BRAM.

``` verilog
module instruction_counter #(
    parameter output_width = 8,
    parameter Num_cycles_for_instruction=10,
    parameter Num_instructions=66753
)(
    input clk,
    input reset,
    output [output_width-1:0]addra_wire
);
```

### Block RAM (Vivado ip)

The Block RAM is used for storing instructions.

### multi-channel control

Instance multiple instruction counters and BRAM ips, and initialize each BRAM ip using the generated `.coe` files

## result given by tweezer experiment

![alt text](/pics/tweezer_result.png)