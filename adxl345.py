import time

from machine import Pin, I2C

ADXL345_ADDR = 83

ADXL345_REG_DEVID = 0x00
# 0x01 ~ 0x1c reserved
ADXL345_REG_THRESH_TAP = 0x1d
ADXL345_REG_OFSX = 0x1e
ADXL345_REG_OFSY = 0x1f
ADXL345_REG_OFSZ = 0x20
ADXL345_REG_DUR = 0x21
ADXL345_REG_LATENT = 0x22
ADXL345_REG_WINDOW = 0x23
ADXL345_REG_THRESH_ACT = 0x24
ADXL345_REG_THRESH_INACT = 0x25
ADXL345_REG_TIME_INACT = 0x26
ADXL345_REG_ACT_INACT_CTL = 0x27
ADXL345_REG_THRESH_FF = 0x28
ADXL345_REG_TIME_FF = 0x29
ADXL345_REG_TAP_AXES = 0x2a
ADXL345_REG_ACT_TAP_STATUS = 0x2b
ADXL345_REG_BW_RATE = 0x2c
ADXL345_REG_POWER_CTL = 0x2d
ADXL345_REG_INT_ENABLE = 0x2e
ADXL345_REG_INT_MAP = 0x2f
ADXL345_REG_INT_SOURCE = 0x30
ADXL345_REG_DATA_FORMAT = 0x31
ADXL345_REG_DATAX0 = 0x32
ADXL345_REG_DATAX1 = 0x33
ADXL345_REG_DATAY0 = 0x34
ADXL345_REG_DATAY1 = 0x35
ADXL345_REG_DATAZ0 = 0x36
ADXL345_REG_DATAZ1 = 0x37
ADXL345_REG_FIFO_CTL = 0x38
ADXL345_REG_FIFO_STATUS = 0x39


class i2c_ifce(object):
    def __init__(self, ifce=0, scl=5, sda=4, freq=100000):
        self.ifce = ifce
        self.scl = scl
        self.sda = sda
        self.freq = freq

        self.i2c = I2C(self.ifce, scl=Pin(self.scl),
                       sda=Pin(self.sda), freq=self.freq);

    def write_byte_data(self, addr, byte, data):
        # print("dump:", data.to_bytes(1, 'little'))
        self.i2c.writeto_mem(addr, byte, data.to_bytes(1, 'little'))

    def write_byte(self, addr, byte):
        self.i2c.writeto(addr, byte)

    def read_byte_data(self, addr, byte):
        # print("dump:", byte)
        return self.i2c.readfrom_mem(addr, byte, 1)

    def read_byte(self, addr):
        return self.i2c.readfrom(addr, 1)

    def i2c_scan(self):
        return self.i2c.scan()


class adxl345(i2c_ifce):

    def __init__(self, dev_addr):
        self.dev_addr = dev_addr
        # initialize i2c interface
        super().__init__()

        # initialize adxl345's power control reg
        super().write_byte_data(self.dev_addr, ADXL345_REG_POWER_CTL, 0)

    def read_device_id(self):
        return super().read_byte_data(self.dev_addr, ADXL345_REG_DEVID)

    def read_thresh_tap(self):
        return super().read_byte_data(self.dev_addr, ADXL345_REG_THRESH_TAP)

    def start_measure(self):
        super().write_byte_data(self.dev_addr, ADXL345_REG_POWER_CTL, 1 << 3)


def main():
    print("Hello World!")
    adxl345_dev = adxl345(ADXL345_ADDR)
    print(adxl345_dev.read_device_id())
    adxl345_dev.start_measure()

    while True:
        print(adxl345_dev.read_thresh_tap())
        time.sleep_ms(200)
        break


if __name__ == "__main__":
    main()
