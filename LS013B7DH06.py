import time

import machine
from machine import Pin, SPI

TFT_HOR_RES = 128   # around to 216 bits in a row actually
TFT_VER_RES = 128

OFFSET_X = 0
OFFSET_Y = 0

g_tft_buf = [0x0] * int(25 * 200)

class tft(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=5000000, sck=Pin(18), mosi=Pin(19))
        self.mod = Pin(15, mode=Pin.OUT, value=1)
        self.inv = Pin(14, mode=Pin.OUT, value=1)
        self.cs = Pin(13, mode=Pin.OUT, value=0)
        self.blk = Pin(12, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)

    def write_byte(self, cmd):
        self.cs.low()
        self.spi.write(bytearray([cmd]))
        self.cs.high()
        # self.spi.write(bytearray([cmd]))

    def init_display(self):
        pass

    def clear(self):
        self.write_byte

    def put_pixel(self, x, y, color):
        ca_slice = int(x / 4)
        addr = int(y / 2) * 48 + ca_slice
        print(x, ca_slice, addr)
        if y % 2 != 0:
            g_tft_buf[addr] |= (0x80 >> (2 * (x % 4) - 2))
        else:
            # TODO: add even rows buffer drawing
            pass

    def flush(self):
        pass

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = tft()
    dev.init_display()
    
    while True:
        dev.inv.low()
        time.sleep_ms(200)
        dev.inv.high()
        time.sleep_ms(200)
        dev.blk.low()
        time.sleep_ms(200)
        dev.blk.high()
        time.sleep_ms(200)

    print("flushing...")
    dev.flush()
    print("done.")