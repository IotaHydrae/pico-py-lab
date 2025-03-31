import time

import machine
from machine import Pin, SPI

BLACK   = 0x00
RED     = 0x04
GREEN   = 0x02
YELLOW  = 0x06
BLUE    = 0x01
MAGENTA = 0x05
CYAN    = 0x03
WHITE   = 0x07



class LS013B7DH06(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=(25 * 1000 * 1000), sck=Pin(18), mosi=Pin(19))
        self.mod = Pin(15, mode=Pin.OUT, value=0)
        self.inv = Pin(14, mode=Pin.OUT, value=0)
        self.cs = Pin(13, mode=Pin.OUT, value=0)
        self.blk = Pin(12, mode=Pin.OUT, value=0)
        self.width = 128
        self.height = 128
        self.line_width = self.width * 3 / 8
        self.framebuffer = [0xff] * int(self.width * self.line_width)

    def reverse_byte(self, n):
        n = ((n & 0b11110000) >> 4) | ((n & 0b00001111) << 4)
        n = ((n & 0b11001100) >> 2) | ((n & 0b00110011) << 2)
        n = ((n & 0b10101010) >> 1) | ((n & 0b01010101) << 1)
        return n

    def spi_write8(self, b):
        b = b.to_bytes(1, "little")
        self.spi.write(b)

    def clear(self):
        self.cs.high()

        self.spi_write8(0x20)
        self.spi_write8(0x00)

        self.cs.low()
        self.cs.high()

    def set_pixel(self, x, y, color):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        # 1 pixel cost 3 bit, so see 8 pixels as a group (3 byte)
        line_buffer = self.framebuffer[y * 48: (y + 1) * 48]
        # print(self.framebuffer[y * 48: (y + 1) * 48])
        # find out the x in which group
        index = int(x * 3 / 24)
        offs = ((x * 3) % 24)
        # print(line_buffer[index * 3: index * 3 + 3])
        group = int.from_bytes(bytes(line_buffer[index * 3: index * 3 + 3]), "little")
        group &= ~(0b111 << offs)
        group |= (color << offs)

        line_buffer[index * 3 + 0] = (group >>  0) & 0xff
        line_buffer[index * 3 + 1] = (group >>  8) & 0xff
        line_buffer[index * 3 + 2] = (group >> 16) & 0xff

        self.framebuffer[y * 48: (y + 1) * 48] = line_buffer
        # print(self.framebuffer[y * 48: (y + 1) * 48])
        pass


    def refresh(self):
        self.cs.high()

        self.spi_write8(0x80)   # Data update mode
        self.spi_write8(0x00)   # first gate line addr

        # send first line
        for i in range(48):
            self.spi_write8(self.framebuffer[i])

        # send last line
        for i in range(0, self.height):
            self.spi_write8(0x00)   # 8 dummy clock
            addr = i + 1
            self.spi_write8(self.reverse_byte(addr))      # current gate line addr

            for k in range(48):
                self.spi_write8(self.reverse_byte(self.framebuffer[i * 48 + k]))

        # 16 dummy clock
        self.spi_write8(0x00)
        self.spi_write8(0x00)

        self.cs.low()
        self.cs.high()

        lcd.blk.low()
        lcd.blk.high()

    def display(self):
        self.cs.high()

        self.spi_write8(0x00)
        self.spi_write8(0x00)

        self.cs.low()
        self.cs.high()

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    lcd = LS013B7DH06()
    lcd.clear()

    # for i in range(256):
    #     lcd.update_line(i, BLACK)

    print("Framebuffer size:", len(lcd.framebuffer))

    for x in range(64):
        lcd.set_pixel(x + 0, 64, GREEN)
        lcd.set_pixel(x + 0, 100, GREEN)

    for x in range(128):
        for y in range(128):
            lcd.set_pixel(x, y, GREEN)

    lcd.refresh()
