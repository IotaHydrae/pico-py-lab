import time

import machine
from machine import Pin, SPI

from imagedata import GDEY037T03_gImage_1

# it's a 16:9 panel
EPD_HOR_RES = 416
EPD_VER_RES = 240
EPD_BUF_LEN = EPD_VER_RES*EPD_HOR_RES/8

g_framebuffer = [0xff]*12480

class GDEY037T03(object):
    def __init__(self):
        self.spi = SPI(1, baudrate=12000000, sck=Pin(10), mosi=Pin(11), miso=Pin(8))

        self.busy = Pin(3, mode=Pin.IN)
        self.rst = Pin(6, mode=Pin.OUT, value=1)
        self.dc = Pin(7, mode=Pin.OUT, value=1)
        self.cs = Pin(9, mode=Pin.OUT, value=1)

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
        # print("reg: ", reg)
        self.write_cmd(reg)

        if len(opts) == 1:
            return

        opts = opts[1:]
        for val in opts:
            # print("val: ", val)
            self.write_data(val)

    def load_reg(self):
        pass

    def wait_busy(self):
        while not self.busy.value():
            continue

    def init_display(self):
        self.reset()

        self.write_reg(0x04)  # power on
        self.wait_busy()

        # vcom and data interval setting
        self.write_reg(0x50, 0x97)  # WBmode:VBDF 17|D7 VBDW 97 VBDB 57    WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7

    def init_display_fast(self):
        self.reset()

        self.write_reg(0x04)
        self.wait_busy()

        self.write_reg(0xe0, 0x02, 0xe5, 0x32)

        # vcom and data interval setting
        self.write_reg(0x50, 0x97)  # WBmode:VBDF 17|D7 VBDW 97 VBDB 57    WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7

    def refresh(self):
        self.write_reg(0x12)
        self.wait_busy()
        pass

    def reset(self):
        self.rst.low()
        time.sleep_us(200)
        self.rst.high()

    def fill(self, color: bool):
        pass

    def clear(self):
        for i in g_framebuffer:
            g_framebuffer[i]=0xff

        self.write_reg(0x10)  # transfer old data
        self.write_data_buffered(g_framebuffer)

        self.write_reg(0x13)  # transfer new data
        self.write_data_buffered(g_framebuffer)

        self.refresh()
        pass

    def show_img(self, img):
        if len(img) != EPD_BUF_LEN:
            print("unsupported img size!")
            return

        self.write_reg(0x10)  # transfer old data
        self.write_data_buffered(img)

        self.write_reg(0x13)  # transfer new data
        self.write_data_buffered(img)

        self.refresh()
        pass

    def sleep(self):
        self.write_reg(0x50, 0xf7)  # VCOM AND DATA INTERVAL SETTING

        self.write_reg(0x02)  # power off
        self.wait_busy()

        self.write_reg(0x07, 0xa5)
        pass


if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = GDEY037T03()

    print("cleaning screen ...")
    dev.init_display()
    dev.clear()
    dev.sleep()

    print("refreshing img ...")
    dev.init_display()
    dev.show_img(GDEY037T03_gImage_1)
    dev.sleep()

    print("System halted ...")
