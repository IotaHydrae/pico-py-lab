import time

import machine
from machine import Pin, SPI

EPD_HOR_RES = 240
EPD_VER_RES = 240

# EPD_BUF_LEN = EPD_HOR_RES

g_tx_buf = [0xffff] * 240 * 10

class ssd1327(object):
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
        # print("reg: ", reg)
        self.write_cmd(reg)

        if len(opts) == 1:
            return

        opts = opts[1:]
        for val in opts:
            # print("val: ", val)
            self.write_data(val)

    def init_display(self):
        self.reset()

        # self.write_cmd(SWRESET)
        self.write_cmd(0x11)

        time.sleep_ms(120)

        self.write_cmd(0x36)
        self.write_data(0x00)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x32)

        # self.write_cmd(0xC0)
        # self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x15)

        self.write_cmd(0xC4)
        self.write_data(0x20) # VDV, 0x20: 0v

        self.write_cmd(0xC6)
        self.write_data(0x0F) # 0x0F: 60 Hz

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        # self.write_cmd(0xD6)
        # self.write_data(0xA1) # sleep in后，gate输出为GND

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x08)
        self.write_data(0x0E)
        self.write_data(0x09)
        self.write_data(0x09)
        self.write_data(0x05)
        self.write_data(0x31)
        self.write_data(0x33)
        self.write_data(0x48)
        self.write_data(0x17)
        self.write_data(0x14)
        self.write_data(0x15)
        self.write_data(0x31)
        self.write_data(0x34)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x08)
        self.write_data(0x0E)
        self.write_data(0x09)
        self.write_data(0x09)
        self.write_data(0x15)
        self.write_data(0x31)
        self.write_data(0x33)
        self.write_data(0x48)
        self.write_data(0x17)
        self.write_data(0x14)
        self.write_data(0x15)
        self.write_data(0x31)
        self.write_data(0x34)

        self.write_cmd(0x21)

        self.write_cmd(0x29)


    def set_cursor(self, x, y):
        self.write_cmd(0x2a)
        self.write_data(0x00)
        self.write_data(x & 0xff)
        self.write_data(0x00)
        self.write_data(0xef)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(y & 0xff)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2c)

    def set_window(self, xs, xe, ys, ye):
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
        time.sleep_ms(100)
        self.rst.low()
        time.sleep_ms(100)
        self.rst.high()

    def put_pixel(self, x, y, color):
        self.set_cursor(x, y)
        self.write_data(color >> 8)
        self.write_data(color & 0xff)

    def clear(self):
        # prepare buffer
        for i in range(len(g_tx_buf)):
            g_tx_buf[i] = 0xff
        self.set_cursor(0, 0)

        for i in range(EPD_HOR_RES * EPD_VER_RES / 240 / 10 * 2):
            self.write_data_buffered(g_tx_buf)

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = ssd1327()
    dev.init_display()

    print("cleaning screen ...")
    dev.clear()

    print("drawing test...")
    # for x in range(240):
    #         dev.put_pixel(x, x, 0xfd2c)

    # for x in range(240):
    #     for y in range(240):
    #         dev.put_pixel(x, y, 0xf12c)

    dev.set_cursor(0, 0)
    for i in range(240 * 240):
        dev.write_data(0xfd)
        dev.write_data(0x2c)

    dev.set_cursor(0, 0)
    for x in range(240):
            dev.put_pixel(x, x - 1, 0xf800)
            dev.put_pixel(x, x, 0xf800)
            dev.put_pixel(x, x+1, 0xf800)
    
    print("done.")