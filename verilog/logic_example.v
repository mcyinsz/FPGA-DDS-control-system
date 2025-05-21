`timescale 1ns / 1ps

module instruction_counter #(
    parameter output_width = 8,
    parameter Num_cycles_for_instruction=10,
    parameter Num_instructions=66753
)
(
    input clk,
    input reset,
    output [output_width-1:0]addra_wire
);
    reg [30:0]count;
    always @(posedge clk or posedge reset) begin
        if (count == Num_cycles_for_instruction || reset) begin
            count <= 0;
        end
        else begin
            count <= count+1;
        end
    end
    
    wire clka;
    assign clka = count == Num_cycles_for_instruction;
    
    reg [16:0]addra;
    always @(posedge clka or posedge reset) begin
        if (reset) begin
            addra<=0;
        end 
        else begin
            if (addra<Num_instructions) begin
                addra <= addra+1;
            end
            else begin
                addra <= addra;
            end
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
        .output_width(17),  // 使用 .参数名(值) 的语法
        .Num_cycles_for_instruction(10),
        .Num_instructions(66583)
    ) ic1 (
        .clk(clk),
        .reset(reset),
        .addra_wire(addra)  // 信号连接
    );
    
    instruction_counter #(
        .output_width(17),  // 使用 .参数名(值) 的语法
        .Num_cycles_for_instruction(10),
        .Num_instructions(66583)
    ) ic2 (
        .clk(clk),
        .reset(reset),
        .addra_wire(addrb)  // 信号连接
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


