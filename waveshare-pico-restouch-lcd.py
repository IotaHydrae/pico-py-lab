import time

import machine
from machine import Pin, SPI

EPD_HOR_RES = 240
EPD_VER_RES = 320

g_tx_buf = [0x00] * 320

class st7789v(object):
    def __init__(self):
        self.spi = SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        self.dc = Pin(8, mode=Pin.OUT, value=1)
        self.cs = Pin(9, mode=Pin.OUT, value=1)
        self.blk = Pin(13, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)
        pass
    def spi_read8(self):
        return self.spi.read()

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

    def set_rotation(self, r):
        self.write_cmd(0x36)
        self.write_data(0)

    def init_display(self):
        self.reset()

        pass
        # self.write_cmd(SWRESET)
        self.write_cmd(0x11)

        time.sleep_ms(120)

        self.write_cmd(0x36)
        self.write_data(0x00)

        self.write_cmd(0x3a)
        self.write_data(0x55)

        self.write_cmd(0xb2)
        self.write_data(0x0c)
        self.write_data(0x0c)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xb7)
        self.write_data(0x35)

        self.write_cmd(0xbb)
        self.write_data(0x28)

        self.write_cmd(0xc0)
        self.write_data(0x3c)

        self.write_cmd(0xc2)
        self.write_data(0x01)

        self.write_cmd(0xc3)
        self.write_data(0x0b)

        self.write_cmd(0xc4)
        self.write_data(0x20) # VDV, 0x20: 0v

        self.write_cmd(0xc6)
        self.write_data(0x0f) # 0x0F: 60 Hz

        self.write_cmd(0xd0)
        self.write_data(0xa4)
        self.write_data(0xa1)

        # self.write_cmd(0xD6)
        # self.write_data(0xA1) # sleep in后，gate输出为GND

        self.write_cmd(0xe0)
        self.write_data(0xd0)
        self.write_data(0x01)
        self.write_data(0x08)
        self.write_data(0x0f)
        self.write_data(0x11)
        self.write_data(0x2a)
        self.write_data(0x36)
        self.write_data(0x55)
        self.write_data(0x44)
        self.write_data(0x3a)
        self.write_data(0x0b)
        self.write_data(0x06)
        self.write_data(0x11)
        self.write_data(0x20)

        self.write_cmd(0xe1)
        self.write_data(0xd0)
        self.write_data(0x02)
        self.write_data(0x07)
        self.write_data(0x0a)
        self.write_data(0x0b)
        self.write_data(0x18)
        self.write_data(0x34)
        self.write_data(0x43)
        self.write_data(0x4a)
        self.write_data(0x2b)
        self.write_data(0x1b)
        self.write_data(0x1c)
        self.write_data(0x22)
        self.write_data(0x1f)

        self.write_cmd(0x55)
        self.write_data(0xb0)

        self.write_cmd(0x29)


    def set_cursor(self, x, y):
        self.write_cmd(0x2a)
        self.write_data(x >> 8)
        self.write_data(x & 0xff)
        self.write_data(0x00)
        self.write_data(0xef)

        self.write_cmd(0x2B)
        self.write_data(y >> 8)
        self.write_data(y & 0xff)
        self.write_data(0x01)
        self.write_data(0x40)
        
        self.write_cmd(0x2c)

    def set_window(self, xs, xe, ys, ye):
        self.write_cmd(0x2a)
        self.write_data(xs >> 8)
        self.write_data(xs & 0xff)
        self.write_data(xe >> 8)
        self.write_data(xe & 0xff)

        self.write_cmd(0x2B)
        self.write_data(ys >> 8)
        self.write_data(ys & 0xff)
        self.write_data(ye >> 8)
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
        self.set_cursor(0, 0)

        for i in range(EPD_HOR_RES * EPD_VER_RES * 2):
            self.write_data(0xff)

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = st7789v()
    dev.init_display()
    dev.set_rotation(0)

    print("cleaning screen ...")
    dev.clear()

    # print("drawing test...")
    for x in range(240):
            dev.put_pixel(x, x, 0xfd2c)

    # for x in range(240):
    #     for y in range(240):
    #         dev.put_pixel(x, y, 0xf12c)

    # dev.set_cursor(0, 0)
    # for i in range(240 * 240):
    #     dev.write_data(0xfd)
    #     dev.write_data(0x2c)
    #
    # dev.set_cursor(0, 0)
    # for x in range(240):
    #         dev.put_pixel(x, x - 1, 0xf800)
    #         dev.put_pixel(x, x, 0xf800)
    #         dev.put_pixel(x, x+1, 0xf800)
    
    print("done.")