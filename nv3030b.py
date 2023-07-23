import time

import machine
from machine import Pin, SPI

EPD_HOR_RES = 240
EPD_VER_RES = 280

EPD_BUF_LEN = EPD_HOR_RES

g_tx_buf = [0x0] * 240

USE_HORIZONTAL = 1
class nv3030b(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=50000000, sck=Pin(18), mosi=Pin(19))
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        self.dc = Pin(14, mode=Pin.OUT, value=1)
        self.cs = Pin(13, mode=Pin.OUT, value=1)
        self.blk = Pin(12, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)
        pass

    def write_cmd(self, cmd):
        self.dc.low()
        self.cs.low()
        self.spi_write8(cmd)
        self.cs.high()
        pass

    def write_data(self, data):
        self.dc.high()
        self.cs.low()
        self.spi_write8(data)
        self.cs.high()
        pass

    def write_data_buffered(self, buf):
        self.dc.high()
        self.cs.low()
        for val in buf:
            self.spi_write8(val)
        self.cs.high()

    def write_reg(self, *opts):
        reg = opts[0]
        print("reg: ", hex(reg))
        self.write_cmd(reg)

        if len(opts) == 1:
            return

        opts = opts[1:]
        for val in opts:
            print("val: ", hex(val))
            self.write_data(val)

    def init_display(self):
        self.reset()
        time.sleep_ms(50)

        self.write_cmd(0xfd)  # private_access
        self.write_data(0x06)
        self.write_data(0x08)

        self.write_cmd(0x61)  # add
        self.write_data(0x07)  #
        self.write_data(0x04)  #

        self.write_cmd(0x62)  # bias setting
        self.write_data(0x00)  # 00
        self.write_data(0x44)  # 44
        self.write_data(0x45)  # 40  47

        self.write_cmd(0x63)  #
        self.write_data(0x41)  #
        self.write_data(0x07)  #
        self.write_data(0x12)  #
        self.write_data(0x12)  #

        self.write_cmd(0x64)  #
        self.write_data(0x37)  #
        #  VSP
        self.write_cmd(0x65)  # Pump1=4.7MHz  #  PUMP1 VSP
        self.write_data(0x09)  # D6-5:pump1_clk[1:0] clamp 28 2b
        self.write_data(0x10)  # 6.26
        self.write_data(0x21)
        #  VSN
        self.write_cmd(0x66)  # pump=2 AVCL
        self.write_data(0x09)  # clamp 08 0b 09
        self.write_data(0x10)  # 10
        self.write_data(0x21)
        #  add source_neg_time
        self.write_cmd(0x67)  # pump_sel
        self.write_data(0x20)  # 21 20
        self.write_data(0x40)

        #  gamma vap/van
        self.write_cmd(0x68)  # gamma vap/van
        self.write_data(0x90)  #
        self.write_data(0x4c)  #
        self.write_data(0x7C)  # VCOM
        self.write_data(0x66)  #

        self.write_cmd(0xb1)  # frame rate
        self.write_data(0x0F)  # 0x0f fr_h[5:0] 0F
        self.write_data(0x02)  # 0x02 fr_v[4:0] 02
        self.write_data(0x01)  # 0x04 fr_div[2:0] 04

        self.write_cmd(0xB4)
        self.write_data(0x01)  # 01:1dot 00:column
        #   #  porch
        self.write_cmd(0xB5)
        self.write_data(0x02)  # 0x02 vfp[6:0]
        self.write_data(0x02)  # 0x02 vbp[6:0]
        self.write_data(0x0a)  # 0x0A hfp[6:0]
        self.write_data(0x14)  # 0x14 hbp[6:0]

        self.write_cmd(0xB6)
        self.write_data(0x04)  #
        self.write_data(0x01)  #
        self.write_data(0x9f)  #
        self.write_data(0x00)  #
        self.write_data(0x02)  #
        #   #  gamme sel
        self.write_cmd(0xdf)  #
        self.write_data(0x11)  # gofc_gamma_en_sel=1
        #   #  gamma_test1 A1 #  _wangly
        #  3030b_gamma_new_
        #  GAMMA--------------------------------- #   #   #   #   #   #  /

        #  GAMMA--------------------------------- #   #   #   #   #   #  /
        self.write_cmd(0xE2)
        self.write_data(0x13)  # vrp0[5:0]	V0 13
        self.write_data(0x00)  # vrp1[5:0]	V1
        self.write_data(0x00)  # vrp2[5:0]	V2
        self.write_data(0x30)  # vrp3[5:0]	V61
        self.write_data(0x33)  # vrp4[5:0]	V62
        self.write_data(0x3f)  # vrp5[5:0]	V63

        self.write_cmd(0xE5)
        self.write_data(0x3f)  # vrn0[5:0]	V63
        self.write_data(0x33)  # vrn1[5:0]	V62
        self.write_data(0x30)  # vrn2[5:0]	V61
        self.write_data(0x00)  # vrn3[5:0]	V2
        self.write_data(0x00)  # vrn4[5:0]	V1
        self.write_data(0x13)  # vrn5[5:0]  V0 13

        self.write_cmd(0xE1)
        self.write_data(0x00)  # prp0[6:0]	V15
        self.write_data(0x57)  # prp1[6:0]	V51

        self.write_cmd(0xE4)
        self.write_data(0x58)  # prn0[6:0]	V51
        self.write_data(0x00)  # prn1[6:0]  V15

        self.write_cmd(0xE0)
        self.write_data(0x01)  # pkp0[4:0]	V3
        self.write_data(0x03)  # pkp1[4:0]	V7
        self.write_data(0x0d)  # pkp2[4:0]	V21
        self.write_data(0x0e)  # pkp3[4:0]	V29
        self.write_data(0x0e)  # pkp4[4:0]	V37
        self.write_data(0x0c)  # pkp5[4:0]	V45
        self.write_data(0x15)  # pkp6[4:0]	V56
        self.write_data(0x19)  # pkp7[4:0]	V60

        self.write_cmd(0xE3)
        self.write_data(0x1a)  # pkn0[4:0]	V60
        self.write_data(0x16)  # pkn1[4:0]	V56
        self.write_data(0x0C)  # pkn2[4:0]	V45
        self.write_data(0x0f)  # pkn3[4:0]	V37
        self.write_data(0x0e)  # pkn4[4:0]	V29
        self.write_data(0x0d)  # pkn5[4:0]	V21
        self.write_data(0x02)  # pkn6[4:0]	V7
        self.write_data(0x01)  # pkn7[4:0]	V3
        #  GAMMA--------------------------------- #   #   #   #   #   #  /

        #  source
        self.write_cmd(0xE6)
        self.write_data(0x00)
        self.write_data(0xff)  # SC_EN_START[7:0] f0

        self.write_cmd(0xE7)
        self.write_data(0x01)  # CS_START[3:0] 01
        self.write_data(0x04)  # scdt_inv_sel cs_vp_en
        self.write_data(0x03)  # CS1_WIDTH[7:0] 12
        self.write_data(0x03)  # CS2_WIDTH[7:0] 12
        self.write_data(0x00)  # PREC_START[7:0] 06
        self.write_data(0x12)  # PREC_WIDTH[7:0] 12

        self.write_cmd(0xE8)  # source
        self.write_data(0x00)  # VCMP_OUT_EN 81-
        self.write_data(0x70)  # chopper_sel[6:4]
        self.write_data(0x00)  # gchopper_sel[6:4] 60
        #   #  gate
        self.write_cmd(0xEc)
        self.write_data(0x52)  # 52

        self.write_cmd(0xF1)
        self.write_data(0x01)  # te_pol tem_extend 00 01 03
        self.write_data(0x01)
        self.write_data(0x02)

        self.write_cmd(0xF6)
        self.write_data(0x09)
        self.write_data(0x10)
        self.write_data(0x00)  #
        self.write_data(0x00)  # 40 3线2通道

        self.write_cmd(0xfd)
        self.write_data(0xfa)
        self.write_data(0xfc)

        self.write_cmd(0x3a)
        self.write_data(0x05)  #

        self.write_cmd(0x35)
        self.write_data(0x00)

        self.write_cmd(0x36)
        self.write_data(0x08)
        # if USE_HORIZONTAL == 0:
        #     self.write_data(0x08)
        # elif USE_HORIZONTAL == 1:
        #     self.write_data(0xC8)
        # elif USE_HORIZONTAL == 2:
        #     self.write_data(0x78)
        # else:
        #     self.write_data(0xA8)

        self.write_cmd(0x21)

        self.write_cmd(0x11)  # exit sleep
        time.sleep_ms(120)
        
        self.write_cmd(0x29)  # display on
        # time.sleep_ms(10)

    def set_window(self, x1, y1, x2, y2):
        y1 += 20
        y2 += 20
        self.write_cmd(0x2a)
        self.write_data(0x0)
        self.write_data(x1 & 0xff)
        self.write_data(0x0)
        self.write_data(x2 & 0xff)

        self.write_cmd(0x2b)
        self.write_data(y1 >> 8)
        self.write_data(y1 & 0xff)

        self.write_data(y2 >> 8)
        self.write_data(y2 & 0xff)
        self.write_cmd(0x2c)
        # if USE_HORIZONTAL == 0:
        #     y1 += 20
        #     y2 += 20
        #     self.write_cmd(0x2a)
        #     self.write_data(0x0)
        #     self.write_data(x1 & 0xff)
        #     self.write_data(0x0)
        #     self.write_data(x2 & 0xff)
        #
        #     self.write_cmd(0x2b)
        #     self.write_data(y1 >> 8)
        #     self.write_data(y1 & 0xff)
        #
        #     self.write_data(y2 >> 8)
        #     self.write_data(y2 & 0xff)
        # elif USE_HORIZONTAL == 1:
        #     y1 += 20
        #     y2 += 20
        #     self.write_cmd(0x2a)
        #     self.write_data(0x0)
        #     self.write_data(x1 & 0xff)
        #     self.write_data(0x0)
        #     self.write_data(x2 & 0xff)
        #
        #     self.write_cmd(0x2b)
        #     self.write_data(y1 >> 8)
        #     self.write_data(y1 & 0xff)
        #
        #     self.write_data(y2 >> 8)
        #     self.write_data(y2 & 0xff)
        # elif USE_HORIZONTAL == 2:
        #     x1 += 20
        #     x2 += 20
        #     self.write_cmd(0x2a)
        #     self.write_data(0x0)
        #     self.write_data(x1 & 0xff)
        #     self.write_data(0x0)
        #     self.write_data(x2 & 0xff)
        #
        #     self.write_cmd(0x2b)
        #     self.write_data(y1 >> 8)
        #     self.write_data(y1 & 0xff)
        #
        #     self.write_data(y2 >> 8)
        #     self.write_data(y2 & 0xff)
        # else:
        #     x1 += 20
        #     x2 += 20
        #     self.write_cmd(0x2a)
        #     self.write_data(0x0)
        #     self.write_data(x1 & 0xff)
        #     self.write_data(0x0)
        #     self.write_data(x2 & 0xff)
        #
        #     self.write_cmd(0x2b)
        #     self.write_data(y1 >> 8)
        #     self.write_data(y1 & 0xff)
        #
        #     self.write_data(y2 >> 8)
        #     self.write_data(y2 & 0xff)

    def reset(self):
        self.rst.high()
        time.sleep_us(100)
        self.rst.low()
        time.sleep_us(100)
        self.rst.high()

    def put_pixel(self, x, y, color):
        self.set_window(x, y, 239, 279)
        self.write_data((color >> 8))
        self.write_data(color & 0xff)

    def clear(self):
        # prepare buffer
        # for i in range(len(g_tx_buf)):
        #     g_tx_buf[i] = 0x0
        self.set_window(0, 0, 239, 279)

        # for i in range(EPD_HOR_RES * EPD_VER_RES / 240 * 2):
        #     self.write_data_buffered(g_tx_buf)
        for i in range(EPD_HOR_RES * EPD_VER_RES * 2):
            self.write_data(0x0)


if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = nv3030b()
    dev.init_display()

    print("cleaning screen ...")
    dev.clear()

    print("drawing test...")

    dev.set_window(0, 0, 240, 280)

    # for x in range(240):
    #     dev.put_pixel(x, x, 0xf800)

    # for x in range(240):
    #     for y in range(280):
    #         dev.put_pixel(x, y, 0xf12c)

    for x in range(240):
        for y in range(280):
            dev.write_data(0xfd)
            dev.write_data(0x2c)

    print("done.")
