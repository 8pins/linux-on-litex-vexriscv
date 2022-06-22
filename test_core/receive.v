module test_receive #(
    // parameter NUM_OUTPUTS = 256,
    // parameter NUM_NEURONS = 256,
    // parameter NUM_AXONS = 256,
    // parameter NUM_TICKS = 16,
    // parameter DX_MSB = 29,
    // parameter DX_LSB = 21,
    // parameter DY_MSB = 20,
    // parameter DY_LSB = 12,
    // parameter PACKET_WIDTH = (DX_MSB - DX_LSB + 1)+(DY_MSB - DY_LSB + 1)+$clog2(NUM_AXONS)+$clog2(NUM_TICKS)
    parameter PACKET_WIDTH = 32
)(
    input clk,
    input rst,
    // input tick,
    // input input_buffer_empty,
    // input [PACKET_WIDTH-1:0] packet,
    // output [$clog2(NUM_OUTPUTS)-1:0] packet_out,
    input [PACKET_WIDTH-1:0] packet_out,
    input packet_out_valid,
    // output ren_to_input_buffer,
    // output token_controller_error,
    // output scheduler_error
    output [PACKET_WIDTH-1:0] packet_in,
    output input_buffer_empty,

    // control i/o
    input read_req

);
    wire wen;
    reg [PACKET_WIDTH-1:0] in;
    reg empty;

    always @(posedge clk) begin
        if (rst) begin
            empty <= 0;
            in <= 0;
        end
        else if (wen) begin
            empty <= 1;
            in <= packet_out;
        end
        else begin
            empty <= 0; 
            in <= 0;           
        end
    end

    assign wen = read_req & (!empty) & packet_out_valid ;
    assign packet_in = in;
    assign input_buffer_empty = empty;

endmodule