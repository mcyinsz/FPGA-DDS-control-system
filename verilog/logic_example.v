`timescale 1ns / 1ps

module instruction_counter #(
    parameter output_width = 8,
    parameter Num_cycles_for_instruction = 10,
    parameter Num_instructions = 66753,
    parameter Delay_cycles = 0
)
(
    input clk,
    input reset,
    output [output_width-1:0] addra_wire
);
    reg [30:0] count;
    reg [31:0] delay_counter;
    reg delay_done;
    reg [16:0] addra;
    
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            delay_counter <= 0;
            delay_done <= (Delay_cycles == 0); 
        end else begin
            if (Delay_cycles == 0) begin
                delay_done <= 1'b1;
            end else if (!delay_done) begin
                if (delay_counter == Delay_cycles - 1) begin
                    delay_done <= 1'b1;
                end
                delay_counter <= delay_counter + 1;
            end
        end
    end

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            count <= 0;
        end else if (delay_done) begin
            if (count == Num_cycles_for_instruction - 1) begin
                count <= 0;
            end else begin
                count <= count + 1;
            end
        end else begin
            count <= 0;
        end
    end
    
    wire clka;
    assign clka = (delay_done && (count == Num_cycles_for_instruction - 1));
    
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            addra <= 0;
        end else if (delay_done && clka) begin
            addra <= (addra < Num_instructions-1) ? addra + 1 : addra;
        end else begin
            addra <= addra;
        end
    end
   
   assign addra_wire = addra;
   
endmodule


module output_with_assistant(
    input clk,
    input reset,
    output [10:0]dataa,
    output [10:0]datab
    );
    wire [10:0]douta;
    wire [10:0]doutb;
    wire ena;
    assign ena=1;
    
    wire [16:0]addra;
    wire [16:0]addrb;
    
    instruction_counter #(
        .output_width(17),  
        .Num_cycles_for_instruction(10),
        .Num_instructions(66583),
        .Delay_cycles(0)
    ) ic1 (
        .clk(clk),
        .reset(reset),
        .addra_wire(addra)  
    );
    
    instruction_counter #(
        .output_width(17),  
        .Num_cycles_for_instruction(10),
        .Num_instructions(66583),
        .Delay_cycles(0)
    ) ic2 (
        .clk(clk),
        .reset(reset),
        .addra_wire(addrb)
    );
   

    
    blk_mem_gen_0 blkmem0 (
      .clka(clk),    // input wire clka
      .ena(ena),      // input wire ena
      .addra(addra),  // input wire [7 : 0] addra
      .douta(douta)  // output wire [10 : 0] douta
    );
    
    assign dataa=douta;
    
    blk_mem_gen_1 blkmem1 (
      .clka(clk),    // input wire clka
      .ena(ena),      // input wire ena
      .addra(addrb),  // input wire [7 : 0] addra
      .douta(doutb)  // output wire [10 : 0] douta
    );
    
    assign datab=doutb;
    
endmodule


