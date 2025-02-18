import time

import machine
from machine import Pin, SPI

TFT_HOR_RES = 128   # around to 216 bits in a row actually
TFT_VER_RES = 128

BLACK   = 0x00
RED     = 0x80
GREEN   = 0x40
YELLOW  = 0xC0
BLUE    = 0x20
MAGENTA = 0xA0
CYAN    = 0x60
WHITE   = 0xE0

OFFSET_X = 0
OFFSET_Y = 0

# g_tft_buf = [0x0] * int(25 * 200)

class tft(object):
    def __init__(self):
        # self.spi = SPI(0, baudrate=1000000, sck=Pin(18), mosi=Pin(19))
        self.sck = Pin(18, mode=Pin.OUT, value=0)
        self.mosi = Pin(19, mode=Pin.OUT, value=0)
        self.mod = Pin(15, mode=Pin.OUT, value=0)
        self.inv = Pin(14, mode=Pin.OUT, value=0)
        self.cs = Pin(13, mode=Pin.OUT, value=0)
        self.blk = Pin(12, mode=Pin.OUT, value=0)

    # def spi_write8(self, b):
    #     self.spi.write(bytearray([b]))
    #     # print(b)

    # def write_byte(self, val):
    #     self.spi_write8(val)

    def spi_writen(self, val, n):
        for i in range(n):
            self.sck.low()
            if val & 0x80:
                self.mosi.high()
            else:
                self.mosi.low()
            self.sck.high()
            val <<= 1
        self.mosi.low()
        self.sck.low()

    def write_bits(self, val, n):
        self.spi_writen(val, n)

    def init_display(self):
        # This driver IC does not have any
        # register for setting the display
        pass

    # see manual page 20, 6-6-4 All Clear Mode
    def clear(self):
        # self.cs.low()
        self.cs.high()

        self.write_bits(0x20, 6)
        self.write_bits(0x00, 2)
        self.write_bits(0x00, 8)

        self.cs.low()

    def fill_color(self, color):
        # self.cs.low()
        self.cs.high()

        self.write_bits(0x80, 6)

        for i in range(256):
            self.write_bits(0x00, 2)
            self.write_bits(i, 8)

            for i in range(128):
                self.write_bits(color, 3)
            self.write_bits(0x00, 6)

        self.write_bits(0x00, 2)
        self.write_bits(0x00, 8)

        self.cs.low()
        self.cs.high()

    def flush(self):
        self.cs.low()
        self.cs.high()
        self.write_bits(0x00, 6)
        self.write_bits(0x00, 2)
        self.write_bits(0x00, 8)

        self.cs.low()

    def put_pixel(self, x, y, color):
        pass

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = tft()
    dev.init_display()

    dev.blk.low()
    dev.clear()
    time.sleep_ms(5)
    dev.blk.high()

    while True:
        dev.fill_color(BLACK)
        time.sleep_ms(500)

        dev.fill_color(RED)
        time.sleep_ms(500)

        dev.fill_color(GREEN)
        time.sleep_ms(500)

        dev.fill_color(YELLOW)
        time.sleep_ms(500)

        dev.fill_color(BLUE)
        time.sleep_ms(500)

        dev.fill_color(MAGENTA)
        time.sleep_ms(500)

        dev.fill_color(CYAN)
        time.sleep_ms(500)

        dev.fill_color(WHITE)
        time.sleep_ms(500)
