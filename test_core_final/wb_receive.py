from migen import *

from litex.soc.interconnect.csr import *
# need interrupt handle?
from litex.soc.interconnect.csr_eventmanager import *

from litex.soc.integration.doc import AutoDoc, ModuleDoc

class RTLreceive (Module, AutoCSR, AutoDoc):
    def __init__(self, platform):
        self.intro = ModuleDoc(""" test_send core""")
        self.control = CSRStorage(fields=[
            CSRField("read_req", size=1, description="packet read request"),
            CSRField("reset", size=1, description="reset control",)
        ])
        self.status = CSRStatus(size=1, fields = [
            CSRField("empty", size=1, description="receive input buffer empty")
        ])
        self.data = CSRStatus(32, reset=0x0, name="packet_in", description="packet_in" )

        read_req = Signal()
        input_buffer_empty = Signal()
        core_reset = Signal()
        self.comb += [
            read_req.eq(self.control.fields.read_req),
            core_reset.eq(self.control.fields.reset),
        ]

        self.status.fields.empty.eq(input_buffer_empty),

        packet_in = Signal()
        self.comb += [
            self.data.status.eq(packet_in)
        ]

        PACKET_WIDTH = 32    
        self.packet_out = Signal()
        self.packet_out_valid = Signal()
        self.specials += Instance("test_receive",
            p_PACKET_WIDTH = PACKET_WIDTH,
            i_clk = ClockSignal(),
            i_rst = ResetSignal() | core_reset,
            i_read_req = read_req,
            o_input_buffer_empty = input_buffer_empty,
            o_packet_in = packet_in,
            i_packet_out = self.packet_out,
            i_packet_out_valid = self.packet_out_valid,
            )

        platform.add_source("./test_core/receive.v")
