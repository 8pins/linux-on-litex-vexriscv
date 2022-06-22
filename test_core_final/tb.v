// Code your testbench here
// or browse Examples
//`include "design.sv"

module top_tb ();
  localparam PW = 32;
  reg [PW-1:0] in, out;
  wire [PW-1:0] recv_output;
  wire recv_input_buffer_empty;
  reg tick, req, input_buffer_empty;
  reg clk, rst;
  
  top #(.PK_W(PW))
  dut
  (
    .clk(clk),
    .rst(rst),
    .tick(tick),
    .packet_in(in),
    .recv_packet_in(recv_output),
    .read_req(req),
    .input_buffer_empty(input_buffer_empty),
    .recv_input_buffer_empty(recv_input_buffer_empty)
  );
  
  initial begin
    clk = 0;
    rst = 0;
    
  end
  
  initial begin
    
    while(1) begin
      #5;
      clk = ~clk;
    end
  end
  
  initial begin
  	$dumpfile("dump.vcd");
    $dumpvars(1);
    #10; 
    rst = 1;
    #10;
    rst = 0;
    in = 32'd32;
   	#10;
    tick = 1;
    input_buffer_empty = 1;
    #10;
    req = 1;
    tick = 0;
    input_buffer_empty = 0;
    #10;
    req = 0;
    in = 32'd256;
    #10;
    tick = 1;
    input_buffer_empty = 1;
    #10;
    req = 1;
    tick = 0;
    
    #30;
    $finish;
  end
  
  initial begin
    assign out = recv_output;
  end
  
  
endmodule