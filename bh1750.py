from machine import Pin, I2C
import time

BH1750_ADDR = 0x23

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
    def __init__(self, ifce=1, scl=3, sda=2, freq=400000):
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


class bh1750(i2c_ifce):
    def __init__(self, addr):
        self.addr = addr
        super().__init__()

    def read_reg(self, reg) -> int:
        return int.from_bytes(super().read_byte_data(self.dev_addr, reg), 'little')

    def write_reg(self, reg, val):
        val = val.to_bytes(1, 'little')
        super().write_byte_data(self.addr, reg, val)

    def power_on(self):
        self.write_reg(self.addr, 0x01)
    
    def power_down(self):
        self.write_reg(self.addr, 0x00)

    def reset(self):
        self.write_reg(self.addr, 0x07)
    
    def set_mode(self, mode):
        self.write_reg(self.addr, mode)
    
    def one_time_low_res_mode(self):
        self.set_mode(0x23)

def main():
    dev = bh1750(BH1750_ADDR)
    for addr in dev.i2c_scan():
        print('addr :', addr)
        if addr == BH1750_ADDR:
            print("BH1750 detected!")

    dev.power_on()
    dev.one_time_low_res_mode()
    time.sleep(0.2)
    print(dev.read_byte())
    print(dev.read_byte())
    dev.power_down()

if __name__ == "__main__":
    main()
