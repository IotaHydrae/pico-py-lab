import time
import ctypes
from machine import Pin, I2C

"""
Device addr of BMP280
"""
BMP280_ADDR = 0x76

"""
Register Map
"""
BMP280_REG_ID         = 0xD0
BMP280_REG_RST        = 0xE0
BMP280_REG_STAT       = 0xF3
BMP280_REG_CTRL_MEAS  = 0xF4
BMP280_REG_CFG        = 0xF5
BMP280_REG_PRESS_MSB  = 0xF7
BMP280_REG_PRESS_LSB  = 0xF8
BMP280_REG_PRESS_XLSB = 0xF9
BMP280_REG_TEMP_MSB   = 0xFA
BMP280_REG_TEMP_LSB   = 0xFB
BMP280_REG_TEMP_XLSB  = 0xFC

bmp280_basic_regs = [
    BMP280_REG_ID         ,
    BMP280_REG_RST        ,
    BMP280_REG_STAT       ,
    BMP280_REG_CTRL_MEAS  ,
    BMP280_REG_CFG        ,
    BMP280_REG_PRESS_MSB  ,
    BMP280_REG_PRESS_LSB  ,
    BMP280_REG_PRESS_XLSB ,
    BMP280_REG_TEMP_MSB   ,
    BMP280_REG_TEMP_LSB   ,
    BMP280_REG_TEMP_XLSB  ,
]

BMP280_CMD_RESET = 0xB6

BMP280_MODE_SLEEP  = 0x00
BMP280_MODE_FORCE  = 0x01
BMP280_MODE_NORMAL = 0x11

bmp280_comp_regs = {
    "dig_T1" : 0x88,    # u16
    "dig_T2" : 0x8A,    # s16
    "dig_T3" : 0x8C,    # s16

    "dig_P1" : 0x8E,    # u16
    "dig_P2" : 0x90,    # s16
    "dig_P3" : 0x92,    # s16
    "dig_P4" : 0x94,    # s16
    "dig_P5" : 0x96,    # s16
    "dig_P6" : 0x98,    # s16
    "dig_P7" : 0x9A,    # s16
    "dig_P8" : 0x9C,    # s16
    "dig_P9" : 0x9E,    # s16

    "reserved" : 0xA0,  # reserved
}

def in_hex(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return hex(res)

    return wrapper

def set_bits(val, mask):
    val |= mask
    return val

def clear_bits(val, mask):
    val &= ~(mask)
    return val

def print_hex(val):
    print(hex(val))

class i2c_ifce(object):
    def __init__(self, ifce=0, scl=5, sda=4, freq=400000):
        self.ifce = ifce
        self.scl = scl
        self.sda = sda
        self.freq = freq

        self.i2c = I2C(self.ifce, scl=Pin(self.scl),
                       sda=Pin(self.sda), freq=self.freq);

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

class bmp280(i2c_ifce):
    def __init__(self, addr):
        self.addr = addr
        super().__init__()

    def read_reg(self, reg) -> int:
        return int.from_bytes(super().read_byte_data(self.addr, reg), 'little')

    def write_reg(self, reg, val):
        val = val.to_bytes(1, 'little')
        super().write_byte_data(self.addr, reg, val)

    def dump_basic_regs(self):
        for reg in bmp280_basic_regs:
            print("Reg: ", hex(reg), ":",hex(self.read_reg(reg)))

    def dump_comp_regs(self):
        for k in bmp280_comp_regs:
            print(k, ":", hex(self.read_reg(bmp280_comp_regs.get(k))))

    @in_hex
    def read_id(self):
        # for bmp280, this should be 0x58
        return self.read_reg(BMP280_REG_ID)

    def reset(self):
        self.write_reg(BMP280_REG_RST, BMP280_CMD_RESET)

    def power_mode(self, mode):
        val = self.read_reg(BMP280_REG_CTRL_MEAS)
        val &= ~(0x03)
        val |= (mode & 0x03)
        self.write_reg(BMP280_REG_CTRL_MEAS, val)

    def read_stat(self):
        return self.read_reg(BMP280_REG_STAT)

    def init(self):
        self.reset()

        self.write_reg(BMP280_REG_CTRL_MEAS, 0x27)

    def measure(self):
        self.power_mode(BMP280_MODE_FORCE)
        while self.read_stat() & 0x08:
            print("waiting ...")

    def temperature(self):
        self.measure()
        dig_T1 = self.read_reg(bmp280_comp_regs.get("dig_T1"))
        dig_T2 = self.read_reg(bmp280_comp_regs.get("dig_T2"))
        dig_T3 = self.read_reg(bmp280_comp_regs.get("dig_T3"))
        print(dig_T1, dig_T2, dig_T3)

        adc_T = self.read_reg(BMP280_REG_TEMP_MSB) << 8 | \
                self.read_reg(BMP280_REG_TEMP_LSB)
        print(adc_T)

        var1 = (((adc_T >> 3) - (dig_T1 << 1)) * dig_T2) >> 11;
        var2 = (((((adc_T >> 4) - (dig_T1)) * ((adc_T >> 4)) - (dig_T1)) >> 12) \
                * dig_T3) >> 14
        
        t_fine = var1 + var2
        
        T = (t_fine * 5 + 128) >> 8
        print(var1, var2, T)
        return T

    def pressure(self):
        pass

def main():
    dev = bmp280(BMP280_ADDR)
    for addr in dev.i2c_scan():
        if addr == BMP280_ADDR:
            print("BMP280 detected!")

    print("ID : ", dev.read_id())
    dev.init()

    dev.temperature()

if __name__ == "__main__":
    main()
