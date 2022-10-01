import sys
import machine
from machine import Pin, I2C, Timer
import lvgl as lv

sys.path.append('.')
from st77xx import *

# from xpt2046 import *

"""
Device addr of ADXL345
"""
ADXL345_ADDR = 83

"""
Register Map
"""
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

"""
Bit Masks -- Register Interrupt Enable
"""
ADXL345_INT_ENABLE_DATA_READY = (1 << 7)
ADXL345_INT_ENABLE_SINGLE_TAP = (1 << 6)
ADXL345_INT_ENABLE_DOUBLE_TAP = (1 << 5)
ADXL345_INT_ENABLE_ACTIVITY = (1 << 4)
ADXL345_INT_ENABLE_INACTIVITY = (1 << 3)
ADXL345_INT_ENABLE_FREE_FALL = (1 << 2)
ADXL345_INT_ENABLE_WATERMARK = (1 << 1)
ADXL345_INT_ENABLE_ACTIVITY_TAP = (1 << 0)

"""

"""


def in_hex(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return hex(res)

    return wrapper


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


class adxl345(i2c_ifce):

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
        # Clear pctl reg
        self.i2c_write(ADXL345_REG_POWER_CTL, 0)
        # Enable measure
        power_ctl: bytes = self.i2c_read(ADXL345_REG_POWER_CTL)
        print(power_ctl)

        self.i2c_write(ADXL345_REG_POWER_CTL, power_ctl | (1 << 3))

        # Enable single tap interrupt
        int_enable = self.i2c_read(ADXL345_REG_INT_ENABLE)
        print("int_enable:", int_enable)
        self.i2c_write(ADXL345_REG_INT_ENABLE,
                       int_enable |
                       ADXL345_INT_ENABLE_DATA_READY |
                       ADXL345_INT_ENABLE_SINGLE_TAP
                       )
        # Set Data format, full res +-16g
        self.i2c_write(ADXL345_REG_DATA_FORMAT, (1 << 3) | 3)

        # Configure FIFO to stream mode
        self.i2c_write(ADXL345_REG_FIFO_CTL, (2 << 6))
        fifo_ctl = self.i2c_read(ADXL345_REG_FIFO_CTL)
        print("fifo ctl:", fifo_ctl)

    @in_hex
    def read_device_id(self) -> int:
        return self.i2c_read(ADXL345_REG_DEVID)

    def read_thresh_tap(self):
        return self.i2c_read(ADXL345_REG_THRESH_TAP)

    def read_int_source(self):
        return self.i2c_read(ADXL345_REG_INT_SOURCE)

    def read_data_x0(self):
        return self.i2c_read(ADXL345_REG_DATAX0)

    def read_data_x1(self):
        return self.i2c_read(ADXL345_REG_DATAX1)

    def read_data_x(self):
        msb = self.read_data_x1()
        lsb = self.read_data_x0()

        return lsb if msb <= 0 else lsb - 255

    def read_data_y0(self):
        return self.i2c_read(ADXL345_REG_DATAY0)

    def read_data_y1(self):
        return self.i2c_read(ADXL345_REG_DATAY1)

    def read_data_y(self):
        msb = self.read_data_y1()
        lsb = self.read_data_y0()

        return lsb if msb <= 0 else lsb - 255

    def read_data_z0(self):
        return self.i2c_read(ADXL345_REG_DATAZ0)

    def read_data_z1(self):
        return self.i2c_read(ADXL345_REG_DATAZ1)

    def read_data_z(self):
        msb = self.read_data_z1()
        lsb = self.read_data_z0()

        return lsb if msb <= 0 else lsb - 255

    def start_measure(self):
        self.i2c_write(ADXL345_REG_POWER_CTL, 1 << 3)


spi = machine.SPI(
    0,
    baudrate=24_000_000,
    polarity=0,
    phase=0,
    sck=machine.Pin(18, machine.Pin.OUT),
    mosi=machine.Pin(19, machine.Pin.OUT),
)

if 0:
    # with DMA, the repaints seem to be too slow? To be investigated
    # we seem to be fine performance-wise without DMA with 320x240 anyway
    import rp2_dma

    rp2_dma = rp2_dma.DMA(0)
else:
    rp2_dma = None

def main():
    print("Hello World!")
    adxl345_dev = adxl345(ADXL345_ADDR)
    print("devid:", adxl345_dev.read_device_id())
    adxl345_dev.start_measure()

    lcd = St7735(rot=3, res=(128, 160),
                 spi=spi, cs=13, dc=14, bl=12, rst=15,
                 rp2_dma=rp2_dma,
                 model='blacktab')
    lcd.set_backlight(100)
    # touch=Xpt2046(spi=spi,cs=16,rot=1,spiPrereadCb=lcd.rp2_wait_dma)
    print("lcd initialized!")

    scr = lv.obj()
    btn = lv.btn(scr)
    btn.align(lv.ALIGN.CENTER, 0, 0)
    label = lv.label(btn)
    label.set_text("Hello World!")

    # Load the screen
    lv.scr_load(scr)

    def update_adxl345(t):
        x = adxl345_dev.read_data_x()
        y = adxl345_dev.read_data_y()
        z = adxl345_dev.read_data_z()
        label.set_text(f"{x},{y},{z}")

    timer = Timer()
    timer.init(mode=Timer.PERIODIC, period=50, callback=update_adxl345)


if __name__ == "__main__":
    main()