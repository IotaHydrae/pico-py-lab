import time

import machine
from machine import Pin, SPI


class xpt2046(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=12000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.penirq = Pin(21, mode=Pin.IN)
        self.cs = Pin(20, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)
        pass

    def is_pressed(self):
        return not self.penirq.value()
    
    def get_x(self):
        self.cs.value(0)
        self.spi_write8(0xd0)
        print(self.spi.read(1))
        print(self.spi.read(1))
        self.cs.value(1)

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = xpt2046()

    while True:
        if dev.is_pressed():
            dev.get_x()
            # get x, y
        
        

    print("done.")