import time

import machine
from machine import Pin, SPI

EPD_HOR_RES = 128
EPD_VER_RES = 128

EPD_BUF_LEN = EPD_HOR_RES

g_tx_buf = [0x0] * 128

class st7735s(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=12000000, sck=Pin(18), mosi=Pin(19))
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

        self.write_reg(0x11)
        time.sleep_ms(120)

        # self.write_reg(0x36, (0x1 << 6) | (0x1 << 2))
        self.write_reg(0x36, 0xff)

        self.write_reg(0x3a, 0x55)

        # self.write_reg(0x21)
        self.write_reg(0x29)

    def set_window(self, xs, xe, ys, ye):
        offset_x = 3
        offset_y = 2

        xs = xs + offset_x
        xe = xe + offset_x
        ys = ys + offset_y
        ye = ye + offset_y
        self.write_cmd(0x2a)
        self.write_data(0x00)
        self.write_data(xs & 0xff)
        self.write_data(0x00)
        self.write_data(xe & 0xff)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(ys & 0xff)
        self.write_data(0x00)
        self.write_data(ye & 0xff)

        self.write_cmd(0x2c)

    def reset(self):
        self.rst.high()
        time.sleep_us(100)
        self.rst.low()
        time.sleep_us(100)
        self.rst.high()

    def put_pixel(self, x, y, color):
        self.set_window(x, 127, y, 127)
        self.write_data((color >> 8))
        self.write_data(color & 0xff)

    def clear(self):
        # prepare buffer
        for i in range(len(g_tx_buf)):
            g_tx_buf[i] = 0x0
        self.set_window(0, 127, 0, 127)

        # for i in range(EPD_HOR_RES * 2):
        #     self.write_data_buffered(g_tx_buf)
        for i in range(EPD_HOR_RES * EPD_VER_RES * 2):
            self.write_data(0xff)


if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = st7735s()
    dev.init_display()

    print("cleaning screen ...")
    dev.clear()

    print("drawing test...")

    for x in range(128):
            dev.put_pixel(x, x, 0xf12c)

    # dev.clear()
    #
    # for x in range(128):
    #     for y in range(128):
    #         dev.put_pixel(x, y, 0xf12c)
    #
    # dev.clear()

    # dev.set_window(0, 127, 0, 127)
    # for x in range(128):
    #     for y in range(128):
    #         dev.write_data(0xfd)
    #         dev.write_data(0x2c)

    print("done.")