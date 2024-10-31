import time

import machine
from machine import Pin, I2C

"""
Device addr of FT6236
"""
FT6236_ADDR = 56

class i2c_ifce(object):
    def __init__(self, ifce=1, scl=27, sda=26, freq=400000):
        self.ifce = ifce
        self.scl = scl
        self.sda = sda
        self.freq = freq

        self.i2c = I2C(self.ifce, scl=Pin(self.scl),
                       sda=Pin(self.sda), freq=self.freq)
    
    def write_byte_data(self, addr, byte, data):
        # print("dump:", data.to_bytes(1, 'little'))
        self.i2c.writeto_mem(addr, byte, data)

    def write_byte(self, addr, byte):
        self.i2c.writeto(addr, byte)

    def read_byte_data(self, addr, byte):
        # print("dump:", byte)
        return self.i2c.readfrom_mem(addr, byte, 1)

    def read_byte(self, addr):
        return self.i2c.readfrom(addr, 1)

    def i2c_scan(self):
        return self.i2c.scan()
    
class ft6236(i2c_ifce):

    def __init__(self, dev_addr):
        self.dev_addr = dev_addr
        # initialize i2c interface
        super().__init__()

        # initialize ft6236's power control reg
        self.init_sequence()

    def i2c_read(self, reg) -> int:
        return int.from_bytes(super().read_byte_data(self.dev_addr, reg), 'little')

    def i2c_write(self, reg, val):
        val = val.to_bytes(1, 'little')
        super().write_byte_data(self.dev_addr, reg, val)

    def init_sequence(self):
        print(self.i2c_read(0xA8))
        pass

if __name__ == "__main__":
    dev = ft6236(FT6236_ADDR)
