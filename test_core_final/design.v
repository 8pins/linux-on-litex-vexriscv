// Code your design here
`include "send.v"
`include "receive.v"

module top #(
  parameter PK_W = 32
)(
  input clk,
  input rst,
  input tick,
  input input_buffer_empty,
  input [PK_W-1:0] packet_in,
  
  output [PK_W-1:0] recv_packet_in,
  output recv_input_buffer_empty,

    // control i/o
  input read_req
);
  
  wire [PK_W-1:0] pkg_o;
  wire pkg_o_valid;
  
  test_send #(.PACKET_WIDTH(PK_W)) send1
  (
    .clk(clk),
    .rst(rst),
    .tick(tick),
 
    .input_buffer_empty(input_buffer_empty),
    .packet_in(packet_in),

    .packet_out(pkg_o),
    .packet_out_valid(pkg_o_valid)
  );
  
  test_receive #(.PACKET_WIDTH(PK_W)) receive1
  (
    .clk(clk),
    .rst(rst),
    .read_req(read_req),
    
    .input_buffer_empty(recv_input_buffer_empty),
    .packet_in(recv_packet_in),
    
    .packet_out(pkg_o),
    .packet_out_valid(pkg_o_valid)
  );
    
endmodule


