module test_send #(
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
    input tick,
    input input_buffer_empty,
    input [PACKET_WIDTH-1:0] packet_in,
    // output [$clog2(NUM_OUTPUTS)-1:0] packet_out,
    output [PACKET_WIDTH-1:0] packet_out,
    output packet_out_valid
    // output ren_to_input_buffer,
    // output token_controller_error,
    // output scheduler_error
);

    wire wen;
    reg [PACKET_WIDTH-1:0] out;
    reg out_valid;

    always @(posedge clk) begin
        if (rst) begin
            out <= 0;
            out_valid <= 0;           
        end
        else if (wen) begin
            out <= packet_in;
            out_valid <= 1;
        end
        else begin
            out <= 0;
            out_valid <= 0;            
        end
    end

    assign wen = tick & input_buffer_empty;
    assign packet_out = out;
    assign packet_out_valid = out_valid;

endmodule




