from migen import *

from litex.soc.interconnect.csr import *
# need interrupt handle?
from litex.soc.interconnect.csr_eventmanager import *

from litex.soc.integration.doc import AutoDoc, ModuleDoc

class RTLsend (Module, AutoCSR, AutoDoc):
    def __init__(self, platform):
        self.intro = ModuleDoc(""" test_send core""")
        self.control = CSRStorage(fields=[
            CSRField("tick", size=1, description="enable tick"),
            CSRField("input_buffer_empty", size=1, description= "receive empty"),
            CSRField("reset", size=1, description="reset control",)
        ])
        self.data = CSRStorage(32, reset=0x0, name="packet_in", description="packet_in" )

        tick = Signal()
        input_buffer_empty = Signal()
        core_reset = Signal()
        self.comb += [
            tick.eq(self.control.fields.tick),
            input_buffer_empty.eq(self.control.fields.input_buffer_empty),
            core_reset.eq(self.control.fields.reset),
        ]

        packet_in = Signal()
        self.comb += [
            packet_in.eq(self.data.storage)
        ]

        PACKET_WIDTH = 32    
        self.packet_out = Signal()
        self.packet_out_valid = Signal()
        self.specials += Instance("test_send",
            p_PACKET_WIDTH = PACKET_WIDTH,
            i_clk = ClockSignal(),
            i_rst = ResetSignal() | core_reset,
            i_tick = tick,
            i_input_buffer_empty = input_buffer_empty,
            i_packet_in = packet_in,
            o_packet_out = self.packet_out,
            o_packet_out_valid = self.packet_out_valid,
            )

        platform.add_source("./test_core/send.v")
