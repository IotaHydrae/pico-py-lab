import time

import machine
from machine import Pin, SPI

COLOR_BLACK            = 0x00
COLOR_BLUE             = 0x02
COLOR_GREEN            = 0x04
COLOR_CYAN             = 0x06
COLOR_RED              = 0x08
COLOR_MAGENTA          = 0x0a
COLOR_YELLOW           = 0x0c
COLOR_WHITE            = 0x0e

# Mode Table
# M0 M1 M2 M3 M4 M5
CMD_NO_UPDATE          = 0x00
CMD_BLINKING_BLACK     = 0x10
CMD_BLINKING_INVERSION = 0x14
CMD_BLINKING_WHITE     = 0x18
CMD_ALL_CLEAR          = 0x20
CMD_VCOM               = 0x40
CMD_UPDATE             = 0x90 # Single Line update mode

DISP_HOR_RES = 176
DISP_VER_RES = 176

class LPM013M126A(object):
    def __init__(self):
        self.spi = SPI(1, baudrate=8000000, sck=Pin(10), mosi=Pin(11), miso=Pin(8))

        self.busy = Pin(3, mode=Pin.IN)
        self.rst = Pin(6, mode=Pin.OUT, value=1)
        # self.dc = Pin(7, mode=Pin.OUT, value=1)
        self.cs = Pin(9, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)
        pass

    def write_cmd(self, cmd):
        # self.dc.low()
        self.cs.high()
        self.spi_write8(cmd)
        self.cs.low()
        pass

    def write_data(self, data):
        # self.dc.high()
        self.cs.high()
        self.spi_write8(data)
        self.cs.low()
        pass

    def write_data_buffered(self, buf):
        # self.dc.high()
        self.cs.high()
        for val in buf:
            self.spi_write8(val)
        self.cs.low()

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

    def clear(self):
        self.write_reg(CMD_ALL_CLEAR, 0);

    def refresh(self):
        self.write_cmd(CMD_UPDATE)

    def init_display(self):
        self.clear()

    def send_line(self, line_buf, line):
        self.cs.high()
        self.spi_write8(CMD_UPDATE)
        self.spi_write8(line+1)
        for i in range(88):
            self.spi_write8(0x88)

        self.spi_write8(0x0)
        self.spi_write8(0x0)
        self.cs.low()

    def refresh(self):
        for line in range(DISP_VER_RES):
            self.send_line(range(88), line)


if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = LPM013M126A()
    dev.init_display()
    dev.refresh()
