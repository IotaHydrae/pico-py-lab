import sys

import time
from machine import Pin, I2C, Timer
import lvgl as lv

sys.path.append('.')
from st77xx import *

"""
Look, These are Registers of DS1307 device
"""
DS1307_REG_SECONDS = 0x00
DS1307_REG_MINUTES = 0x01
DS1307_REG_HOURS = 0x02
DS1307_REG_DAY = 0x03
DS1307_REG_DATE = 0x04
DS1307_REG_MONTH = 0x05
DS1307_REG_YEAR = 0x06
DS1307_REG_CONTROL = 0x07
# RAM 56 x 8
DS1307_REG_RAM_00 = 0x08
DS1307_REG_RAM_55 = 0x3F


class i2c_ifce(object):
    def __init__(self, ifce=0, scl=5, sda=4, freq=100000):
        self.ifce = ifce
        self.scl = scl
        self.sda = sda
        self.freq = freq

        self.i2c = I2C(self.ifce, scl=Pin(self.scl),
                       sda=Pin(self.sda), freq=self.freq)

    def write_byte_data(self, addr, byte, data):
        # print("dump:", data.to_bytes(1, 'little'))
        self.i2c.writeto_mem(addr, byte, data)

    def read_byte_data(self, addr, byte):
        # print("dump:", byte)
        return self.i2c.readfrom_mem(addr, byte, 1)

    def write_byte(self, addr, byte):
        self.i2c.writeto(addr, byte)

    def read_byte(self, addr):
        return self.i2c.readfrom(addr, 1)

    def i2c_scan(self):
        return self.i2c.scan()


class ds1307(i2c_ifce):

    def __init__(self, dev_addr):
        self.dev_addr = dev_addr
        # initialize i2c interface
        super().__init__()

        # initialize adxl345's power control reg
        self.init_sequence()

    def i2c_read(self, reg) -> int:
        return int.from_bytes(super().read_byte_data(self.dev_addr, reg), 'little')

    def i2c_write(self, reg, val):
        val = val.to_bytes(1, 'little')
        super().write_byte_data(self.dev_addr, reg, val)

    def init_sequence(self):
        # Get date from internet (optional)

        # Enable clock
        seconds = self.i2c_read(DS1307_REG_SECONDS)
        self.i2c_write(DS1307_REG_SECONDS, seconds & (~0x80))
        pass

    def dump_ram(self):
        reg_list = []
        for ram_addr in range(56):
            reg_list.append(self.i2c_read(ram_addr))
        print(reg_list)
        return reg_list

spi = machine.SPI(
    0,
    baudrate=50_000_000,
    polarity=0,
    phase=0,
    sck=machine.Pin(18, machine.Pin.OUT),
    mosi=machine.Pin(19, machine.Pin.OUT),
)

def main():
    # lcd = St7735(rot=3, res=(128, 160),
    #              spi=spi, cs=13, dc=14, bl=12, rst=15,
    #              model='blacktab')
    # lcd.set_backlight(80)
    #
    # scr = lv.obj()
    # btn = lv.btn(scr)
    # btn.align(lv.ALIGN.CENTER, 0, 0)
    # label = lv.label(btn)
    # label.set_text("Hello World!")
    #
    # # Load the screen
    # lv.scr_load(scr)
    i2c = i2c_ifce()
    print(i2c.i2c_scan())

    ds1307_dev = ds1307(0x68)
    while True:
        print(ds1307_dev.i2c_read(DS1307_REG_SECONDS))
        # ds1307_dev.dump_ram()
        time.sleep_ms(1000)

if __name__ == "__main__":
    main()
