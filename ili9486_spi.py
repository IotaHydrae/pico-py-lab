import time
import machine
from machine import Pin, SPI

DISP_HOR_RES = 480
DISP_VER_RES = 320

g_tx_buf = [0x0] * DISP_HOR_RES

class ili9486_spi(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=60_000_000, sck=Pin(18), mosi=Pin(19))
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        self.dc = Pin(27, mode=Pin.OUT, value=1)
        self.cs = Pin(17, mode=Pin.OUT, value=1)

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
        # print("reg: ", hex(reg))
        self.write_cmd(reg)

        if len(opts) == 1:
            return

        opts = opts[1:]
        for val in opts:
            # print("val: ", hex(val))
            self.write_data(val)

    def reset(self):
        self.rst.high()
        time.sleep_us(100)
        self.rst.low()
        time.sleep_us(100)
        self.rst.high()

    def init_display(self):
        self.reset()

        self.write_reg(0xf1, 0x36, 0x04, 0x00, 0x3c, 0x0f, 0x8f)
        self.write_reg(0xf2, 0x18, 0xa3, 0x12, 0x02, 0xb2, 0x12, 0xff, 0x10, 0x00)
        self.write_reg(0xf8, 0x21, 0x04)
        self.write_reg(0xf9, 0x00, 0x08)
        self.write_reg(0x36, 0x08)
        self.write_reg(0xb4, 0x00)
        self.write_reg(0xc1, 0x47)
        self.write_reg(0xc5, 0x00, 0xaf, 0x80, 0x00)
        self.write_reg(0xe0, 0x0f, 0x1f, 0x1c, 0x0c, 0x0f, 0x08, 0x48, 0x98, 0x37, 0x0a, 0x13, 0x04, 0x11, 0x0d, 0x00)
        self.write_reg(0xe1, 0x0f, 0x32, 0x2e, 0x0b, 0x0d, 0x05, 0x47, 0x75, 0x37, 0x06, 0x10, 0x03, 0x24, 0x20, 0x00)
        self.write_reg(0x3a, 0x55)
        self.write_reg(0x11)
        self.write_reg(0x36, 0x28)
        time.sleep_ms(120)
        self.write_reg(0x29)

    def set_window(self, xs, xe, ys, ye):
        # offset_x = 20
        # offset_y = 20

        # xs = xs + offset_x
        # xe = xe + offset_x
        # ys = ys + offset_y
        # ye = ye + offset_y
        self.write_cmd(0x2a)
        self.write_data((xs >> 8) & 0xff)
        self.write_data(xs & 0xff)
        self.write_data((xe >> 8) & 0xff)
        self.write_data(xe & 0xff)

        self.write_cmd(0x2b)
        self.write_data((ys >> 8) & 0xff)
        self.write_data(ys & 0xff)
        self.write_data((ye >> 8) & 0xff)
        self.write_data(ye & 0xff)

        self.write_cmd(0x2c)

    def clear(self):
        for i in range(len(g_tx_buf)):
            g_tx_buf[i] = 0
        # self.set_window(0, 127, 0, 127)
        self.set_window(0, DISP_HOR_RES - 1, 0, DISP_VER_RES - 1)

        for i in range(DISP_VER_RES * 2):
            self.write_data_buffered(g_tx_buf)

if __name__ == "__main__":
    print("resettng the cpu freq...")
    print("before:")
    print(machine.freq())
    print("after:")
    machine.freq(240000000)
    print(machine.freq())

    dev = ili9486_spi()
    dev.init_display()
    print("clearing whole screen...")
    dev.clear()