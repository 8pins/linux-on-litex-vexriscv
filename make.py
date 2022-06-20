#!/usr/bin/env python3

#
# This file is part of Linux-on-LiteX-VexRiscv
#
# Copyright (c) 2019-2022, Linux-on-LiteX-VexRiscv Developers
# SPDX-License-Identifier: BSD-2-Clause

import os
import sys
import argparse

from litex.soc.integration.builder import Builder
from litex.soc.cores.cpu.vexriscv_smp import VexRiscvSMP

from soc_linux import SoCLinux

# Board Definition ---------------------------------------------------------------------------------

class Board:
    soc_kwargs = {
        "integrated_rom_size"  : 0x10000,
        "integrated_sram_size" : 0x1800,
        "l2_size"              : 0
    }
    def __init__(self, soc_cls=None, soc_capabilities={}, soc_constants={}):
        self.soc_cls          = soc_cls
        self.soc_capabilities = soc_capabilities
        self.soc_constants    = soc_constants

    def load(self, filename):
        prog = self.platform.create_programmer()
        prog.load_bitstream(filename)

    def flash(self, filename):
        prog = self.platform.create_programmer()
        prog.flash(0, filename)

#---------------------------------------------------------------------------------------------------
# Xilinx Boards
#---------------------------------------------------------------------------------------------------

# Acorn support ------------------------------------------------------------------------------------

class Acorn(Board):
    soc_kwargs = {"uart_name": "jtag_uart", "sys_clk_freq": int(150e6)}
    def __init__(self):
        from litex_boards.targets import acorn
        Board.__init__(self, acorn.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "sata",
        })

# Acorn PCIe support -------------------------------------------------------------------------------

class AcornPCIe(Board):
    soc_kwargs = {"uart_name": "crossover", "sys_clk_freq": int(125e6)}
    def __init__(self):
        from litex_boards.targets import sqrl_acorn
        Board.__init__(self, sqrl_acorn.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "pcie",
        })

    def flash(self, filename):
        prog = self.platform.create_programmer()
        prog.flash(0, filename.replace(".bin", "_fallback.bin"))

# Arty support -------------------------------------------------------------------------------------

class Arty(Board):
    def __init__(self):
        from litex_boards.targets import arty
        Board.__init__(self, arty.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Storage
            "spiflash",
            "sdcard",
            # GPIOs
            "leds",
            "rgb_led",
            "switches",
            # Buses
            "spi",
            "i2c",
            # Monitoring
            "xadc",
            # 7-Series specific
            "mmcm",
            "icap_bitstream",
        })

class ArtyA7(Arty): pass

class ArtyS7(Board):
    def __init__(self):
        from litex_boards.targets import arty_s7
        Board.__init__(self, arty_s7.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "spiflash",
            # GPIOs
            "leds",
            "rgb_led",
            "switches",
            # Buses
            "spi",
            "i2c",
            # Monitoring
            "xadc",
            # 7-Series specific
            "mmcm",
            "icap_bitstream",
        })

# NeTV2 support ------------------------------------------------------------------------------------

class NeTV2(Board):
    def __init__(self):
        from litex_boards.targets import netv2
        Board.__init__(self, netv2.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Storage
            "sdcard",
            # GPIOs
            "leds",
            # Video
            "framebuffer",
            # Monitoring
            "xadc",
        })

# Genesys2 support ---------------------------------------------------------------------------------

class Genesys2(Board):
    def __init__(self):
        from litex_boards.targets import genesys2
        Board.__init__(self, genesys2.BaseSoC, soc_capabilities={
            # Communication
            "usb_fifo",
            "ethernet",
            # Storage
            "sdcard",
        })

# KC705 support ---------------------------------------------------------------------------------

class KC705(Board):
    def __init__(self):
        from litex_boards.targets import xilinx_kc705
        Board.__init__(self, xilinx_kc705.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Storage
            "sdcard",
            #"sata",
            # GPIOs
            "leds",
            # Monitoring
            "xadc",
        })

# VC707 support ---------------------------------------------------------------------------------

class VC707(Board):
    def __init__(self):
        from litex_boards.targets import vc707
        Board.__init__(self, vc707.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Storage
            "sdcard",
            # GPIOs
            "leds",
            # Monitoring
            "xadc",
        })

# KCU105 support -----------------------------------------------------------------------------------

class KCU105(Board):
    def __init__(self):
        from litex_boards.targets import kcu105
        Board.__init__(self, kcu105.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Storage
            "sdcard",
        })

# ZCU104 support -----------------------------------------------------------------------------------

class ZCU104(Board):
    def __init__(self):
        from litex_boards.targets import zcu104
        Board.__init__(self, zcu104.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        })

# Nexys4DDR support --------------------------------------------------------------------------------

class Nexys4DDR(Board):
    def __init__(self):
        from litex_boards.targets import nexys4ddr
        Board.__init__(self, nexys4ddr.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Storage
            "sdcard",
            # Video
            "framebuffer",
        })

# NexysVideo support -------------------------------------------------------------------------------

class NexysVideo(Board):
    def __init__(self):
        from litex_boards.targets import nexys_video
        Board.__init__(self, nexys_video.BaseSoC, soc_capabilities={
            # Communication
            "usb_fifo",
            # Storage
            "sdcard",
            # Video
            "framebuffer",
        })

# MiniSpartan6 support -----------------------------------------------------------------------------

class MiniSpartan6(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import minispartan6
        Board.__init__(self, minispartan6.BaseSoC, soc_capabilities={
            # Communication
            "usb_fifo",
            # Storage
            "sdcard",
            # Video
            "framebuffer",
        })

# Pipistrello support ------------------------------------------------------------------------------

class Pipistrello(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import pipistrello
        Board.__init__(self, pipistrello.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        })

# XCU1525 support ----------------------------------------------------------------------------------

class XCU1525(Board):
    def __init__(self):
        from litex_boards.targets import xcu1525
        Board.__init__(self, xcu1525.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "sata",
        })

# AlveoU280 (ES1) support -------------------------------------------------------------------------------

class AlveoU280(Board):
    soc_kwargs = {
        "with_hbm"     : True, # Use HBM @ 250MHz (Min).
        "sys_clk_freq" : 250e6
    }
    def __init__(self):
        from litex_boards.targets import alveo_u280
        Board.__init__(self, alveo_u280.BaseSoC, soc_capabilities={
            # Communication
            "serial"
        })

# AlveoU250 support -------------------------------------------------------------------------------

class AlveoU250(Board):
    def __init__(self):
        from litex_boards.targets import alveo_u250
        Board.__init__(self, alveo_u250.BaseSoC, soc_capabilities={
            # Communication
            "serial"
        })

# SDS1104X-E support -------------------------------------------------------------------------------

class SDS1104XE(Board):
    soc_kwargs = {"l2_size" : 8192} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import sds1104xe
        Board.__init__(self, sds1104xe.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Video
            "framebuffer",
        })

    def load(self, filename):
        prog = self.platform.create_programmer()
        prog.load_bitstream(filename, device=1)

# QMTECH WuKong support ---------------------------------------------------------------------------

class Qmtech_WuKong(Board):
    def __init__(self):
        from litex_boards.targets import qmtech_wukong
        Board.__init__(self, qmtech_wukong.BaseSoC, soc_capabilities={
            "leds",
            # Communication
            "serial",
            "ethernet",
            # Video
            "framebuffer",
        })


# MNT RKX7 support ---------------------------------------------------------------------------------

class MNT_RKX7(Board):
    def __init__(self):
        from litex_boards.targets import mnt_rkx7
        Board.__init__(self, mnt_rkx7.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "spisdcard",
        })

# STLV7325 -----------------------------------------------------------------------------------------

class STLV7325(Board):
    def __init__(self):
        from litex_boards.targets import stlv7325
        Board.__init__(self, stlv7325.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "sdcard",
        })

# Decklink Quad HDMI Recorder ----------------------------------------------------------------------

class DecklinkQuadHDMIRecorder(Board):
    soc_kwargs = {"uart_name": "crossover",  "sys_clk_freq": int(125e6)}
    def __init__(self):
        from litex_boards.targets import decklink_quad_hdmi_recorder
        Board.__init__(self, decklink_quad_hdmi_recorder.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "pcie",
        })

#---------------------------------------------------------------------------------------------------
# Lattice Boards
#---------------------------------------------------------------------------------------------------

# Versa ECP5 support -------------------------------------------------------------------------------

class VersaECP5(Board):
    def __init__(self):
        from litex_boards.targets import versa_ecp5
        Board.__init__(self, versa_ecp5.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
        })

# ULX3S support ------------------------------------------------------------------------------------

class ULX3S(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import ulx3s
        Board.__init__(self, ulx3s.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "sdcard",
            # Video,
            "framebuffer",
        })

# HADBadge support ---------------------------------------------------------------------------------

class HADBadge(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import hadbadge
        Board.__init__(self, hadbadge.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        })

    def load(self, filename):
        os.system("dfu-util --alt 2 --download {} --reset".format(filename))

# OrangeCrab support -------------------------------------------------------------------------------

class OrangeCrab(Board):
    soc_kwargs = {"sys_clk_freq" : int(64e6) } # Increase sys_clk_freq to 64MHz (48MHz default).
    def __init__(self):
        from litex_boards.targets import orangecrab
        os.system("git clone https://github.com/litex-hub/valentyusb -b hw_cdc_eptri")
        sys.path.append("valentyusb") # FIXME: do proper install of ValentyUSB.
        Board.__init__(self, orangecrab.BaseSoC, soc_capabilities={
            # Communication
            "usb_acm",
            # Buses
            "i2c",
            # Storage
            "sdcard",
        })

# Butterstick support ------------------------------------------------------------------------------

class ButterStick(Board):
    soc_kwargs = {"uart_name": "jtag_uart"}
    def __init__(self):
        from litex_boards.targets import butterstick
        Board.__init__(self, butterstick.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
        })

# Cam Link 4K support ------------------------------------------------------------------------------

class CamLink4K(Board):
    def __init__(self):
        from litex_boards.targets import camlink_4k
        Board.__init__(self, camlink_4k.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        })

    def load(self, filename):
        os.system("camlink configure {}".format(filename))

# TrellisBoard support -----------------------------------------------------------------------------

class TrellisBoard(Board):
    def __init__(self):
        from litex_boards.targets import trellisboard
        Board.__init__(self, trellisboard.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "sdcard",
        })

# ECPIX5 support -----------------------------------------------------------------------------------

class ECPIX5(Board):
    def __init__(self):
        from litex_boards.targets import ecpix5
        Board.__init__(self, ecpix5.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
            # Storage
            "sdcard",
        })

# Colorlight i5 support ----------------------------------------------------------------------------

class Colorlight_i5(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import colorlight_i5
        Board.__init__(self, colorlight_i5.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            "ethernet",
        })

# Icesugar Pro support -----------------------------------------------------------------------------

class IcesugarPro(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import muselab_icesugar_pro
        Board.__init__(self, muselab_icesugar_pro.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "spiflash",
            "sdcard",
        })

#---------------------------------------------------------------------------------------------------
# Intel Boards
#---------------------------------------------------------------------------------------------------

# De10Nano support ---------------------------------------------------------------------------------

class De10Nano(Board):
    soc_kwargs = {
        "with_mister_sdram" : True, # Add MiSTer SDRAM extension.
        "l2_size"           : 2048, # Use Wishbone and L2 for memory accesses.
    }
    def __init__(self):
        from litex_boards.targets import de10nano
        Board.__init__(self, de10nano.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "sdcard",
            # GPIOs
            "leds",
            "switches",
        })

# De0Nano support ----------------------------------------------------------------------------------

class De0Nano(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import de0nano
        Board.__init__(self, de0nano.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        })

# De1-SoC support ----------------------------------------------------------------------------------

class De1SoC(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import de1soc
        Board.__init__(self, de1soc.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # GPIOs
            "leds",
            "switches",
        })

# QMTECH EP4CE15 support ---------------------------------------------------------------------------

class Qmtech_EP4CE15(Board):
    soc_kwargs = {
        "variant" : "ep4ce15",
        "l2_size" : 2048, # Use Wishbone and L2 for memory accesses.
        "integrated_sram_size" : 0x800,
    }
    def __init__(self):
        from litex_boards.targets import qmtech_ep4cex5
        Board.__init__(self, qmtech_ep4cex5.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        })

# ... and its bigger brother 

class Qmtech_EP4CE55(Board):
    soc_kwargs = {
        "variant" : "ep4ce55",
        "l2_size" :  2048, # Use Wishbone and L2 for memory accesses.
    }
    def __init__(self):
        from litex_boards.targets import qmtech_ep4cex5
        Board.__init__(self, qmtech_ep4cex5.BaseSoC, soc_capabilities={
            # Communication
            "serial",
        })

#---------------------------------------------------------------------------------------------------
# Efinix Boards
#---------------------------------------------------------------------------------------------------

class TrionT120BGA576DevKit(Board):
    soc_kwargs = {"l2_size" : 2048} # Use Wishbone and L2 for memory accesses.
    def __init__(self):
        from litex_boards.targets import trion_t120_bga576_dev_kit
        Board.__init__(self, trion_t120_bga576_dev_kit.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # GPIOs
             "leds",
        })

class TitaniumTi60F225DevKit(Board):
    soc_kwargs = {
        "with_hyperram" : True,
        "sys_clk_freq"  : 300e6,
    }
    def __init__(self):
        from litex_boards.targets import titanium_ti60_f225_dev_kit
        Board.__init__(self, titanium_ti60_f225_dev_kit.BaseSoC, soc_capabilities={
            # Communication
            "serial",
            # Storage
            "sdcard",
            # GPIOs
            "leds",
        })

#---------------------------------------------------------------------------------------------------
# Build
#---------------------------------------------------------------------------------------------------

supported_boards = {
    # Xilinx
    "acorn"                       : Acorn,
    "acorn_pcie"                  : AcornPCIe,
    "arty"                        : Arty,
    "arty_a7"                     : ArtyA7,
    "arty_s7"                     : ArtyS7,
    "netv2"                       : NeTV2,
    "genesys2"                    : Genesys2,
    "kc705"                       : KC705,
    "vc707"                       : VC707,
    "kcu105"                      : KCU105,
    "zcu104"                      : ZCU104,
    "nexys4ddr"                   : Nexys4DDR,
    "nexys_video"                 : NexysVideo,
    "minispartan6"                : MiniSpartan6,
    "pipistrello"                 : Pipistrello,
    "xcu1525"                     : XCU1525,
    "alveo_u280"                  : AlveoU280,
    "alveo_u250"                  : AlveoU250,
    "qmtech_wukong"               : Qmtech_WuKong,
    "sds1104xe"                   : SDS1104XE,
    "mnt_rkx7"                    : MNT_RKX7,
    "stlv7325"                    : STLV7325,
    "decklink_quad_hdmi_recorder" : DecklinkQuadHDMIRecorder,

    # Lattice
    "versa_ecp5"                  : VersaECP5,
    "ulx3s"                       : ULX3S,
    "hadbadge"                    : HADBadge,
    "orangecrab"                  : OrangeCrab,
    "butterstick"                 : ButterStick,
    "camlink_4k"                  : CamLink4K,
    "trellisboard"                : TrellisBoard,
    "ecpix5"                      : ECPIX5,
    "colorlight_i5"               : Colorlight_i5,
    "icesugar_pro"                : IcesugarPro,

    # Altera/Intel
    "de0nano"                     : De0Nano,
    "de10nano"                    : De10Nano,
    "de1soc"                      : De1SoC,
    "qmtech_ep4ce15"              : Qmtech_EP4CE15,
    "qmtech_ep4ce55"              : Qmtech_EP4CE55,

    # Efinix
    "trion_t120_bga576_dev_kit"   : TrionT120BGA576DevKit,
    "titanium_ti60_f225_dev_kit"  : TitaniumTi60F225DevKit,
    }

def main():
    description = "Linux on LiteX-VexRiscv\n\n"
    description += "Available boards:\n"
    for name in sorted(supported_boards.keys()):
        description += "- " + name + "\n"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--board",          required=True,               help="FPGA board.")
    parser.add_argument("--device",         default=None,                help="FPGA device.")
    parser.add_argument("--variant",        default=None,                help="FPGA board variant.")
    parser.add_argument("--toolchain",      default=None,                help="Toolchain use to build.")
    parser.add_argument("--uart-baudrate",  default=115.2e3, type=float, help="UART baudrate.")
    parser.add_argument("--build",          action="store_true",         help="Build bitstream.")
    parser.add_argument("--load",           action="store_true",         help="Load bitstream (to SRAM).")
    parser.add_argument("--flash",          action="store_true",         help="Flash bitstream/images (to Flash).")
    parser.add_argument("--doc",            action="store_true",         help="Build documentation.")
    parser.add_argument("--local-ip",       default="192.168.1.50",      help="Local IP address.")
    parser.add_argument("--remote-ip",      default="192.168.1.100",     help="Remote IP address of TFTP server.")
    parser.add_argument("--spi-data-width", default=8,   type=int,       help="SPI data width (max bits per xfer).")
    parser.add_argument("--spi-clk-freq",   default=1e6, type=int,       help="SPI clock frequency.")
    parser.add_argument("--fdtoverlays",    default="",                  help="Device Tree Overlays to apply.")
    VexRiscvSMP.args_fill(parser)
    args = parser.parse_args()
    
    # print(str(args))
    # args la 1 namespace (dictionary)

    # Board(s) selection ---------------------------------------------------------------------------
    if args.board == "all":
        board_names = list(supported_boards.keys())
    else:
        args.board = args.board.lower()
        args.board = args.board.replace(" ", "_")
        board_names = [args.board]

    # Board(s) iteration ---------------------------------------------------------------------------
    for board_name in board_names:
        board = supported_boards[board_name]()
        soc_kwargs = Board.soc_kwargs
        soc_kwargs.update(board.soc_kwargs)

        # CPU parameters ---------------------------------------------------------------------------

        # If Wishbone Memory is forced, enabled L2 Cache (if not already):
        if args.with_wishbone_memory:
            soc_kwargs["l2_size"] = max(soc_kwargs["l2_size"], 2048) # Defaults to 2048.
        # Else if board is configured to use L2 Cache, force use of Wishbone Memory on VexRiscv-SMP.
        else:
            args.with_wishbone_memory = soc_kwargs["l2_size"] != 0

        VexRiscvSMP.args_read(args)

        # SoC parameters ---------------------------------------------------------------------------
        if args.device is not None:
            soc_kwargs.update(device=args.device)
        if args.variant is not None:
            soc_kwargs.update(variant=args.variant)
        if args.toolchain is not None:
            soc_kwargs.update(toolchain=args.toolchain)

        # UART.
        soc_kwargs["uart_baudrate"] = int(args.uart_baudrate)
        if "crossover" in board.soc_capabilities:
            soc_kwargs.update(uart_name="crossover")
        if "usb_fifo" in board.soc_capabilities:
            soc_kwargs.update(uart_name="usb_fifo")
        if "usb_acm" in board.soc_capabilities:
            soc_kwargs.update(uart_name="usb_acm")

        # Peripherals
        if "leds" in board.soc_capabilities:
            soc_kwargs.update(with_led_chaser=True)
        if "ethernet" in board.soc_capabilities:
            soc_kwargs.update(with_ethernet=True)
        if "pcie" in board.soc_capabilities:
            soc_kwargs.update(with_pcie=True)
        if "spiflash" in board.soc_capabilities:
            soc_kwargs.update(with_spi_flash=True)
        if "sata" in board.soc_capabilities:
            soc_kwargs.update(with_sata=True)
        if "video_terminal" in board.soc_capabilities:
            soc_kwargs.update(with_video_terminal=True)
        if "framebuffer" in board.soc_capabilities:
            soc_kwargs.update(with_video_framebuffer=True)

        # SoC creation -----------------------------------------------------------------------------
        soc = SoCLinux(board.soc_cls, **soc_kwargs)
        board.platform = soc.platform

        # SoC constants ----------------------------------------------------------------------------
        for k, v in board.soc_constants.items():
            soc.add_constant(k, v)

        # SoC peripherals --------------------------------------------------------------------------
        if board_name in ["arty", "arty_a7"]:
            from litex_boards.platforms.arty import _sdcard_pmod_io
            board.platform.add_extension(_sdcard_pmod_io)

        if board_name in ["orangecrab"]:
            from litex_boards.platforms.orangecrab import feather_i2c
            board.platform.add_extension(feather_i2c)

        if "mmcm" in board.soc_capabilities:
            soc.add_mmcm(2)
        if "spisdcard" in board.soc_capabilities:
            soc.add_spi_sdcard()
        if "sdcard" in board.soc_capabilities:
            soc.add_sdcard()
        if "ethernet" in board.soc_capabilities:
            soc.configure_ethernet(local_ip=args.local_ip, remote_ip=args.remote_ip)
        #if "leds" in board.soc_capabilities:
        #    soc.add_leds()
        if "rgb_led" in board.soc_capabilities:
            soc.add_rgb_led()
        if "switches" in board.soc_capabilities:
            soc.add_switches()
        if "spi" in board.soc_capabilities:
            soc.add_spi(args.spi_data_width, args.spi_clk_freq)
        if "i2c" in board.soc_capabilities:
            soc.add_i2c()
        if "xadc" in board.soc_capabilities:
            soc.add_xadc()
        if "icap_bitstream" in board.soc_capabilities:
            soc.add_icap_bitstream()

        # add test_core
        soc.add_test_core() 

        # Build ------------------------------------------------------------------------------------
        build_dir = os.path.join("build", board_name)
        builder   = Builder(soc,
            output_dir   = os.path.join("build", board_name),
            bios_options = ["TERM_MINI"],
            csr_json     = os.path.join(build_dir, "csr.json"),
            csr_csv      = os.path.join(build_dir, "csr.csv")
        )
        builder.build(run=args.build, build_name=board_name)

        # DTS --------------------------------------------------------------------------------------
        soc.generate_dts(board_name)
        soc.compile_dts(board_name, args.fdtoverlays)

        # DTB --------------------------------------------------------------------------------------
        soc.combine_dtb(board_name, args.fdtoverlays)

        # PCIe Driver ------------------------------------------------------------------------------
        if "pcie" in board.soc_capabilities:
            from litepcie.software import generate_litepcie_software
            generate_litepcie_software(soc, os.path.join(builder.output_dir, "driver"))

        # Load FPGA bitstream ----------------------------------------------------------------------
        if args.load:
            board.load(filename=builder.get_bitstream_filename(mode="sram"))

        # Flash bitstream/images (to SPI Flash) ----------------------------------------------------
        if args.flash:
            board.flash(filename=builder.get_bitstream_filename(mode="flash"))

        # Generate SoC documentation ---------------------------------------------------------------
        if args.doc:
            soc.generate_doc(board_name)

        

# TYPES OF OBJECTS

    #    print(type(board))  # class __main__.KC705
    #    print(type(soc))    # class soc_linux.SoCLinux.<locals>._SocLinux
    #    print(type(board.soc_cls))

# ARGUMENTS DEBUG
    
    #f_args_debug = open('debug_args.txt','w+')
    #f_args_debug.write(str(args))
    #f_args_debug.close()

# PROPERTIES OF OBJECTS

    from pprint import pprint

    # "board" properties

    # pprint(vars(board))
        # {'platform': <litex_boards.platforms.xilinx_kc705.Platform object at 0x7fdd7365ef10>,
        #  'soc_capabilities': {'ethernet', 'sdcard', 'serial', 'xadc', 'leds'},
        #  'soc_cls': <class 'litex_boards.targets.xilinx_kc705.BaseSoC'>,
        #  'soc_constants': {}}

    # pprint(vars(board.soc_cls))
        # mappingproxy({'__doc__': None,
        #               '__init__': <function BaseSoC.__init__ at 0x7fdd7340d700>,
        #               '__module__': 'litex_boards.targets.xilinx_kc705'})

    # pprint(vars(board.platform))
        # {'constraint_manager': <litex.build.generic_platform.ConstraintManager object at 0x7fd6827c6130>,
        #  'device': 'xc7k325t-ffg900-2',
        #  'edifs': set(),
        #  'finalized': True,
        #  'ips': {},
        #  'name': 'xilinx_kc705',
        #  'output_dir': '/home/eightpins/litex/linux-on-litex-vexriscv/build/kc705',
        #  'sources': [('/home/eightpins/litex/pythondata-cpu-vexriscv-smp/pythondata_cpu_vexriscv_smp/verilog/Ram_1w_1rs_Generic.v',
        #               'verilog',
        #               'work'),
        #              ('/home/eightpins/litex/pythondata-cpu-vexriscv-smp/pythondata_cpu_vexriscv_smp/verilog/VexRiscvLitexSmpCluster_Cc2_Iw64Is8192Iy2_Dw64Ds8192Dy2_ITs4DTs4_Ldw512_Cdma_Ood.v',
        #               'verilog',
        #               'work'),
        #              ('/home/eightpins/litex/linux-on-litex-vexriscv/build/kc705/gateware/kc705.v',
        #               'verilog',
        #               'work')],
        #  'toolchain': <litex.build.xilinx.vivado.XilinxVivadoToolchain object at 0x7fd6825c0e80>,
        #  'use_default_clk': False,
        #  'verilog_include_paths': []}

    # pprint(board.soc_capabilities)
        # {'ethernet', 'sdcard', 'serial', 'xadc', 'leds'}

    # "soc" properties
    
    #f_soc_debug = open('debug_soc.txt','w+')
    # for key, value in vars(soc):
    #     print(key, file=f_soc_debug)
    #     print(value, file = f_soc_debug)
    # pprint(vars(soc.send_core.wb_send.RTLsend.specials))
    # pprint(vars(soc.recv_core.packet_out))
    #f_soc_debug.close()

    # print(vars(soc))
        # {'_fragment': <migen.fhdl.structure._Fragment object at 0x7f9cecda8d90>,
        # '_submodules': [('crg',
        #                 <litex_boards.targets.xilinx_kc705._CRG object at 0x7f9cece33a60>),
        #                 ('bus',
        #                 <litex.soc.integration.soc.SoCBusHandler object at 0x7f9cecdebfd0>),
        #                 ('csr',
        #                 <litex.soc.integration.soc.SoCCSRHandler object at 0x7f9cecdebfa0>),
        #                 ('irq',
        #                 <litex.soc.integration.soc.SoCIRQHandler object at 0x7f9cecdfb070>),
        #                 ('ctrl',
        #                 <litex.soc.integration.soc.SoCController object at 0x7f9cecdfb250>),
        #                 ('cpu',
        #                 <litex.soc.cores.cpu.vexriscv_smp.core.VexRiscvSMP object at 0x7f9cecdfb1f0>),
        #                 ('dma_bus',
        #                 <litex.soc.integration.soc.SoCBusHandler object at 0x7f9cecd999d0>),
        #                 (None,
        #                 <litex.soc.interconnect.wishbone.Converter object at 0x7f9cecda8190>),
        #                 ('rom',
        #                 <litex.soc.interconnect.wishbone.SRAM object at 0x7f9cecdb3b50>),
        #                 ('sram',
        #                 <litex.soc.interconnect.wishbone.SRAM object at 0x7f9cecd42220>),
        #                 ('identifier',
        #                 <litex.soc.cores.identifier.Identifier object at 0x7f9cecd4d580>),
        #                 ('uart_phy',
        #                 <litex.soc.cores.uart.RS232PHY object at 0x7f9cecd555b0>),
        #                 ('uart', <litex.soc.cores.uart.UART object at 0x7f9cecd7dd30>),
        #                 ('timer0',
        #                 <litex.soc.cores.timer.Timer object at 0x7f9ceccee370>),
        #                 ('ddrphy',
        #                 <litedram.phy.s7ddrphy.K7DDRPHY object at 0x7f9cecceb7c0>),
        #                 ('sdram',
        #                 <litedram.core.LiteDRAMCore object at 0x7f9cec67cc40>),
        #                 ('ethphy',
        #                 <liteeth.phy.gmii_mii.LiteEthPHYGMIIMII object at 0x7f9cec135610>),
        #                 ('ethmac', <liteeth.mac.LiteEthMAC object at 0x7f9cec06f7c0>),
        #                 ('leds',
        #                 <litex.soc.cores.led.LedChaser object at 0x7f9cebd18790>),
        #                 ('sdphy', <litesdcard.phy.SDPHY object at 0x7f9cebd18ca0>),
        #                 ('sdcore', <litesdcard.core.SDCore object at 0x7f9cebd358e0>),
        #                 ('sdblock2mem',
        #                 <litesdcard.frontend.dma.SDBlock2MemDMA object at 0x7f9cebb012b0>),
        #                 ('sdmem2block',
        #                 <litesdcard.frontend.dma.SDMem2BlockDMA object at 0x7f9cebacbb20>),
        #                 ('sdirq',
        #                 <litex.soc.interconnect.csr_eventmanager.EventManager object at 0x7f9ceba9a7f0>),
        #                 ('xadc', <litex.soc.cores.xadc.XADC object at 0x7f9cebaa51c0>),
        #                 ('csr_bridge',
        #                 <litex.soc.interconnect.wishbone.Wishbone2CSR object at 0x7f9ceb7e8b80>),
        #                 ('bus_interconnect',
        #                 <litex.soc.interconnect.wishbone.InterconnectShared object at 0x7f9ceb7eddc0>),
        #                 ('dma_bus_interconnect',
        #                 <litex.soc.interconnect.wishbone.InterconnectShared object at 0x7f9ceb7edb80>),
        #                 ('csr_bankarray',
        #                 <litex.soc.interconnect.csr_bus.CSRBankArray object at 0x7f9ceb799940>),
        #                 ('csr_interconnect',
        #                 <litex.soc.interconnect.csr_bus.InterconnectShared object at 0x7f9ceb799970>)],
        # 'build_name': 'kc705',
        # 'bus': <litex.soc.integration.soc.SoCBusHandler object at 0x7f9cecdebfd0>,
        # 'bus_interconnect': <litex.soc.interconnect.wishbone.InterconnectShared object at 0x7f9ceb7eddc0>,
        # 'clk_freq': 125000000,
        # 'config': {},
        # 'constants': {'CONFIG_BUS_ADDRESS_WIDTH': 32,
        #             'CONFIG_BUS_BURSTING': 0,
        #             'CONFIG_BUS_DATA_WIDTH': 32,
        #             'CONFIG_BUS_STANDARD': 'WISHBONE',
        #             'CONFIG_CLOCK_FREQUENCY': 125000000,
        #             'CONFIG_CPU_COUNT': 2,
        #             'CONFIG_CPU_HAS_DMA_BUS': None,
        #             'CONFIG_CPU_HAS_INTERRUPT': None,
        #             'CONFIG_CPU_HUMAN_NAME': 'VexRiscv SMP-LINUX',
        #             'CONFIG_CPU_NOP': 'nop',
        #             'CONFIG_CPU_RESET_ADDR': 0,
        #             'CONFIG_CPU_TYPE_VEXRISCV_SMP': None,
        #             'CONFIG_CPU_VARIANT_LINUX': None,
        #             'CONFIG_CSR_ALIGNMENT': 32,
        #             'CONFIG_CSR_DATA_WIDTH': 32,
        #             'CPU_DCACHE_BLOCK_SIZE': 64,
        #             'CPU_DCACHE_SIZE': 8192,
        #             'CPU_DCACHE_WAYS': 2,
        #             'CPU_DTLB_SIZE': 4,
        #             'CPU_DTLB_WAYS': 4,
        #             'CPU_ICACHE_BLOCK_SIZE': 64,
        #             'CPU_ICACHE_SIZE': 8192,
        #             'CPU_ICACHE_WAYS': 2,
        #             'CPU_ISA': 'rv32ima',
        #             'CPU_ITLB_SIZE': 4,
        #             'CPU_ITLB_WAYS': 4,
        #             'ETHMAC_INTERRUPT': 2,
        #             'ETHMAC_RX_SLOTS': 2,
        #             'ETHMAC_SLOT_SIZE': 2048,
        #             'ETHMAC_TX_SLOTS': 2,
        #             'LOCALIP1': 192,
        #             'LOCALIP2': 168,
        #             'LOCALIP3': 1,
        #             'LOCALIP4': 50,
        #             'REMOTEIP1': 192,
        #             'REMOTEIP2': 168,
        #             'REMOTEIP3': 1,
        #             'REMOTEIP4': 100,
        #             'SDIRQ_INTERRUPT': 3,
        #             'TIMER0_INTERRUPT': 1,
        #             'UART_INTERRUPT': 0},
        # 'cpu': <litex.soc.cores.cpu.vexriscv_smp.core.VexRiscvSMP object at 0x7f9cecdfb1f0>,
        # 'cpu_type': 'vexriscv_smp',
        # 'cpu_variant': 'linux',
        # 'crg': <litex_boards.targets.xilinx_kc705._CRG object at 0x7f9cece33a60>,
        # 'csr': <litex.soc.integration.soc.SoCCSRHandler object at 0x7f9cecdebfa0>,
        # 'csr_bankarray': <litex.soc.interconnect.csr_bus.CSRBankArray object at 0x7f9ceb799940>,
        # 'csr_bridge': <litex.soc.interconnect.wishbone.Wishbone2CSR object at 0x7f9ceb7e8b80>,
        # 'csr_data_width': 32,
        # 'csr_interconnect': <litex.soc.interconnect.csr_bus.InterconnectShared object at 0x7f9ceb799970>,
        # 'csr_regions': {'ctrl': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb55d6d0>,
        #                 'ddrphy': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb55d8e0>,
        #                 'ethmac': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566100>,
        #                 'ethphy': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566190>,
        #                 'identifier_mem': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb5667c0>,
        #                 'leds': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566220>,
        #                 'sdblock2mem': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb5662b0>,
        #                 'sdcore': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566340>,
        #                 'sdirq': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb5663d0>,
        #                 'sdmem2block': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566460>,
        #                 'sdphy': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb5664f0>,
        #                 'sdram': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566580>,
        #                 'timer0': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566610>,
        #                 'uart': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb5666a0>,
        #                 'xadc': <litex.soc.integration.soc.SoCCSRRegion object at 0x7f9ceb566730>},
        # 'ctrl': <litex.soc.integration.soc.SoCController object at 0x7f9cecdfb250>,
        # 'ddrphy': <litedram.phy.s7ddrphy.K7DDRPHY object at 0x7f9cecceb7c0>,
        # 'dma_bus': <litex.soc.integration.soc.SoCBusHandler object at 0x7f9cecd999d0>,
        # 'dma_bus_interconnect': <litex.soc.interconnect.wishbone.InterconnectShared object at 0x7f9ceb7edb80>,
        # 'ethmac': <liteeth.mac.LiteEthMAC object at 0x7f9cec06f7c0>,
        # 'ethphy': <liteeth.phy.gmii_mii.LiteEthPHYGMIIMII object at 0x7f9cec135610>,
        # 'finalized': True,
        # 'get_fragment_called': True,
        # 'identifier': <litex.soc.cores.identifier.Identifier object at 0x7f9cecd4d580>,
        # 'integrated_main_ram_size': 0,
        # 'integrated_rom_initialized': False,
        # 'integrated_rom_size': 65536,
        # 'integrated_sram_size': 6144,
        # 'irq': <litex.soc.integration.soc.SoCIRQHandler object at 0x7f9cecdfb070>,
        # 'leds': <litex.soc.cores.led.LedChaser object at 0x7f9cebd18790>,
        # 'logger': <Logger SoC (INFO)>,
        # 'mem_map': {'clint': 4026597376,
        #             'csr': 4026531840,
        #             'main_ram': 1073741824,
        #             'plic': 4039114752,
        #             'rom': 0,
        #             'sram': 268435456},
        # 'mem_regions': {'clint': <litex.soc.integration.soc.SoCRegion object at 0x7f9cecdb34c0>,
        #                 'csr': <litex.soc.integration.soc.SoCRegion object at 0x7f9ceb7edb50>,
        #                 'ethmac': <litex.soc.integration.soc.SoCRegion object at 0x7f9cebd181c0>,
        #                 'main_ram': <litex.soc.integration.soc.SoCRegion object at 0x7f9cecc924c0>,
        #                 'opensbi': <litex.soc.integration.soc.SoCRegion object at 0x7f9cecda8160>,
        #                 'plic': <litex.soc.integration.soc.SoCRegion object at 0x7f9cecda8df0>,
        #                 'rom': <litex.soc.integration.soc.SoCRegion object at 0x7f9cecd421f0>,
        #                 'sram': <litex.soc.integration.soc.SoCRegion object at 0x7f9cecd4d0d0>},
        # 'platform': <litex_boards.platforms.xilinx_kc705.Platform object at 0x7f9ced019f10>,
        # 'rom': <litex.soc.interconnect.wishbone.SRAM object at 0x7f9cecdb3b50>,
        # 'sdblock2mem': <litesdcard.frontend.dma.SDBlock2MemDMA object at 0x7f9cebb012b0>,
        # 'sdcore': <litesdcard.core.SDCore object at 0x7f9cebd358e0>,
        # 'sdirq': <litex.soc.interconnect.csr_eventmanager.EventManager object at 0x7f9ceba9a7f0>,
        # 'sdmem2block': <litesdcard.frontend.dma.SDMem2BlockDMA object at 0x7f9cebacbb20>,
        # 'sdphy': <litesdcard.phy.SDPHY object at 0x7f9cebd18ca0>,
        # 'sdram': <litedram.core.LiteDRAMCore object at 0x7f9cec67cc40>,
        # 'sram': <litex.soc.interconnect.wishbone.SRAM object at 0x7f9cecd42220>,
        # 'sys_clk_freq': 125000000,
        # 'timer0': <litex.soc.cores.timer.Timer object at 0x7f9ceccee370>,
        # 'uart': <litex.soc.cores.uart.UART object at 0x7f9cecd7dd30>,
        # 'uart_phy': <litex.soc.cores.uart.RS232PHY object at 0x7f9cecd555b0>,
        # 'wb_slaves': {},
        # 'xadc': <litex.soc.cores.xadc.XADC object at 0x7f9cebaa51c0>}

    #pprint(vars(soc.cpu))  
 
    # {'_fragment': <migen.fhdl.structure._Fragment object at 0x7f4f3a7af940>,
    # '_submodules': [],
    # 'clintbus': <Record adr:dat_w:dat_r:sel:cyc:stb:ack:we:cti:bte:err at 0x7f4f3a7c94f0>,
    # 'cpu_params': {'i_clintWishbone_ADR': <Signal clintbus_adr at 0x7f4f3a7c9520>,
    #                 'i_clintWishbone_CYC': <Signal clintbus_cyc at 0x7f4f3a7c9760>,
    #                 'i_clintWishbone_DAT_MOSI': <Signal clintbus_dat_w at 0x7f4f3a7c95b0>,
    #                 'i_clintWishbone_STB': <Signal clintbus_stb at 0x7f4f3a7c97f0>,
    #                 'i_clintWishbone_WE': <Signal clintbus_we at 0x7f4f3a7c9910>,
    #                 'i_dBridge_dram_cmd_ready': <Signal cmd_ready at 0x7f4f39b16f10>,
    #                 'i_dBridge_dram_rdata_payload_data': <Signal rdata_payload_data at 0x7f4f39b26a60>,
    #                 'i_dBridge_dram_rdata_valid': <Signal rdata_valid at 0x7f4f39b267c0>,
    #                 'i_dBridge_dram_wdata_ready': <Signal wdata_ready at 0x7f4f39b263d0>,
    #                 'i_debugCd_external_clk': <migen.fhdl.structure.ClockSignal object at 0x7f4f3a7a25b0>,
    #                 'i_debugCd_external_reset': <migen.fhdl.structure._Operator object at 0x7f4f3a7a2c70>,
    #                 'i_debugPort_capture': <Signal jtag_capture at 0x7f4f3a811220>,
    #                 'i_debugPort_enable': <Signal jtag_enable at 0x7f4f3a7a2100>,
    #                 'i_debugPort_reset': <Signal jtag_reset at 0x7f4f3a7a2310>,
    #                 'i_debugPort_shift': <Signal jtag_shift at 0x7f4f3a7a21f0>,
    #                 'i_debugPort_tdi': <Signal jtag_tdi at 0x7f4f3a7a2430>,
    #                 'i_debugPort_update': <Signal jtag_update at 0x7f4f3a7a2280>,
    #                 'i_dma_wishbone_ADR': <Signal dma_bus_adr at 0x7f4f3a7a2d30>,
    #                 'i_dma_wishbone_CYC': <Signal dma_bus_cyc at 0x7f4f3a7a2fa0>,
    #                 'i_dma_wishbone_DAT_MOSI': <Signal dma_bus_dat_w at 0x7f4f3a7a2df0>,
    #                 'i_dma_wishbone_SEL': <Signal dma_bus_sel at 0x7f4f3a7a2f10>,
    #                 'i_dma_wishbone_STB': <migen.fhdl.structure._Operator object at 0x7f4f3a7af520>,
    #                 'i_dma_wishbone_WE': <Signal dma_bus_we at 0x7f4f3a7af190>,
    #                 'i_iBridge_dram_cmd_ready': <Signal cmd_ready at 0x7f4f39b160a0>,
    #                 'i_iBridge_dram_rdata_payload_data': <Signal rdata_payload_data at 0x7f4f39b16bb0>,
    #                 'i_iBridge_dram_rdata_valid': <Signal rdata_valid at 0x7f4f39b16910>,
    #                 'i_iBridge_dram_wdata_ready': <Signal wdata_ready at 0x7f4f39b16520>,
    #                 'i_interrupts': <Signal interrupt at 0x7f4f3a7a24c0>,
    #                 'i_jtag_clk': <Signal jtag_clk at 0x7f4f3a7a2070>,
    #                 'i_peripheral_ACK': <Signal pbus_ack at 0x7f4f3a7a2910>,
    #                 'i_peripheral_DAT_MISO': <Signal pbus_dat_r at 0x7f4f3a7a26d0>,
    #                 'i_peripheral_ERR': <Signal pbus_err at 0x7f4f3a7a2b50>,
    #                 'i_plicWishbone_ADR': <Signal plicbus_adr at 0x7f4f3a7bde50>,
    #                 'i_plicWishbone_CYC': <Signal plicbus_cyc at 0x7f4f3a7c90d0>,
    #                 'i_plicWishbone_DAT_MOSI': <Signal plicbus_dat_w at 0x7f4f3a7bdee0>,
    #                 'i_plicWishbone_STB': <Signal plicbus_stb at 0x7f4f3a7c9160>,
    #                 'i_plicWishbone_WE': <Signal plicbus_we at 0x7f4f3a7c9280>,
    #                 'o_clintWishbone_ACK': <Signal clintbus_ack at 0x7f4f3a7c9880>,
    #                 'o_clintWishbone_DAT_MISO': <Signal clintbus_dat_r at 0x7f4f3a7c9640>,
    #                 'o_dBridge_dram_cmd_payload_addr': <Signal cmd_payload_addr at 0x7f4f39b261f0>,
    #                 'o_dBridge_dram_cmd_payload_we': <Signal cmd_payload_we at 0x7f4f39b26160>,
    #                 'o_dBridge_dram_cmd_valid': <Signal cmd_valid at 0x7f4f39b16e80>,
    #                 'o_dBridge_dram_rdata_ready': <Signal rdata_ready at 0x7f4f39b26850>,
    #                 'o_dBridge_dram_wdata_payload_data': <Signal wdata_payload_data at 0x7f4f39b265e0>,
    #                 'o_dBridge_dram_wdata_payload_we': <Signal wdata_payload_we at 0x7f4f39b26670>,
    #                 'o_dBridge_dram_wdata_valid': <Signal wdata_valid at 0x7f4f39b26340>,
    #                 'o_debugPort_tdo': <Signal jtag_tdo at 0x7f4f3a7a23a0>,
    #                 'o_dma_wishbone_ACK': <Signal dma_bus_ack at 0x7f4f3a7af100>,
    #                 'o_dma_wishbone_DAT_MISO': <Signal dma_bus_dat_r at 0x7f4f3a7a2e80>,
    #                 'o_dma_wishbone_STALL': <Signal dma_bus_stall at 0x7f4f3a7a2d00>,
    #                 'o_iBridge_dram_cmd_payload_addr': <Signal cmd_payload_addr at 0x7f4f39b16340>,
    #                 'o_iBridge_dram_cmd_payload_we': <Signal cmd_payload_we at 0x7f4f39b162b0>,
    #                 'o_iBridge_dram_cmd_valid': <Signal cmd_valid at 0x7f4f39b92fd0>,
    #                 'o_iBridge_dram_rdata_ready': <Signal rdata_ready at 0x7f4f39b169a0>,
    #                 'o_iBridge_dram_wdata_payload_data': <Signal wdata_payload_data at 0x7f4f39b16730>,
    #                 'o_iBridge_dram_wdata_payload_we': <Signal wdata_payload_we at 0x7f4f39b167c0>,
    #                 'o_iBridge_dram_wdata_valid': <Signal wdata_valid at 0x7f4f39b16490>,
    #                 'o_peripheral_ADR': <Signal pbus_adr at 0x7f4f3a7a25e0>,
    #                 'o_peripheral_BTE': <Signal pbus_bte at 0x7f4f3a7a2ac0>,
    #                 'o_peripheral_CTI': <Signal pbus_cti at 0x7f4f3a7a2a30>,
    #                 'o_peripheral_CYC': <Signal pbus_cyc at 0x7f4f3a7a27f0>,
    #                 'o_peripheral_DAT_MOSI': <Signal pbus_dat_w at 0x7f4f3a7a2580>,
    #                 'o_peripheral_SEL': <Signal pbus_sel at 0x7f4f3a7a2760>,
    #                 'o_peripheral_STB': <Signal pbus_stb at 0x7f4f3a7a2880>,
    #                 'o_peripheral_WE': <Signal pbus_we at 0x7f4f3a7a29a0>,
    #                 'o_plicWishbone_ACK': <Signal plicbus_ack at 0x7f4f3a7c91f0>,
    #                 'o_plicWishbone_DAT_MISO': <Signal plicbus_dat_r at 0x7f4f3a7bdf70>},
    # 'dma_bus': <Record adr:dat_w:dat_r:sel:cyc:stb:ack:we:cti:bte:err at 0x7f4f3a7a2cd0>,
    # 'finalized': True,
    # 'get_fragment_called': True,
    # 'human_name': 'VexRiscv SMP-LINUX',
    # 'interrupt': <Signal interrupt at 0x7f4f3a7a24c0>,
    # 'jtag_capture': <Signal jtag_capture at 0x7f4f3a811220>,
    # 'jtag_clk': <Signal jtag_clk at 0x7f4f3a7a2070>,
    # 'jtag_enable': <Signal jtag_enable at 0x7f4f3a7a2100>,
    # 'jtag_reset': <Signal jtag_reset at 0x7f4f3a7a2310>,
    # 'jtag_shift': <Signal jtag_shift at 0x7f4f3a7a21f0>,
    # 'jtag_tdi': <Signal jtag_tdi at 0x7f4f3a7a2430>,
    # 'jtag_tdo': <Signal jtag_tdo at 0x7f4f3a7a23a0>,
    # 'jtag_update': <Signal jtag_update at 0x7f4f3a7a2280>,
    # 'memory_buses': [<litedram.common.LiteDRAMNativePort object at 0x7f4f39c78f10>,
    #                 <litedram.common.LiteDRAMNativePort object at 0x7f4f39b168e0>],
    # 'pbus': <Record adr:dat_w:dat_r:sel:cyc:stb:ack:we:cti:bte:err at 0x7f4f3a7a2550>,
    # 'periph_buses': [<Record adr:dat_w:dat_r:sel:cyc:stb:ack:we:cti:bte:err at 0x7f4f3a7a2550>],
    # 'platform': <litex_boards.platforms.xilinx_kc705.Platform object at 0x7f4f3aa2ef10>,
    # 'plicbus': <Record adr:dat_w:dat_r:sel:cyc:stb:ack:we:cti:bte:err at 0x7f4f3a7bde20>,
    # 'reset': <Signal reset at 0x7f4f3a811c40>,
    # 'reset_address': 0,
    # 'use_rom': True,
    # 'variant': 'linux'}
if __name__ == "__main__":
    main()
