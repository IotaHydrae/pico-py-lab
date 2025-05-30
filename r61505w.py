import time

import machine
from machine import Pin, SPI

TFT_HOR_RES = 240
TFT_VER_RES = 320

'''
This script is used to test the r61505w based
TFT display which working in SPI mode on the RP2040
'''

R61505W_ID = 0xC505

'''
Register Selection (Clock Synchronous Serial Interface) (page 12)

Start Byte
RW      RS      Function
0       0       Write index to IR
1       0       Setting disabled
0       1       Write to control register or internal frame memory via WDR
1       1       Read from internal frame memory and register via RDR
'''

R61505W_CMD_SET_IR  = 0x70
R61505W_CMD_SET_WDR = 0x72
R61505W_CMD_GET_RDR = 0x73

'''
Index Register (IR) (page 42)

RW RS IB15 IB14 IB13 IB12 IB11 IB10 IB9 IB8 IB7 IB6 IB5 IB4 IB3 IB2 IB1 IB0
 W  0  *    *    *     *    *    *   *   *   ID  ID  ID  ID  ID  ID  ID  ID
                                             [7] [6] [5] [4] [3] [2] [1] [0]

The index register specifies the index R00h to RFFh of the control register
or frame memory control to be accessed using a binary number from “0000_0000”
to “1111_1111”. The access to the register and instruction bits in it is
prohibited unless the index is specified in the index register.
'''

R61505W_REG_ID = 0x00
R61505W_REG_DRV_OUTPUT_CTRL = 0x01
R61505W_REG_ENTRY_MODE = 0x03
R61505W_REG_DISP_CTRL1 = 0x07
R61505W_REG_POW_CTRL1 = 0x10
R61505W_REG_POW_CTRL2 = 0x11
R61505W_REG_POW_CTRL3 = 0x12
R61505W_REG_POW_CTRL4 = 0x13
R61505W_REG_X_ADDR = 0x20
R61505W_REG_Y_ADDR = 0x21
R61505W_REG_MEM_WRITE = 0x22

R61505W_REG_NVM_CTRL4 = 0xA4

class r61505w(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=20000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        # self.dc = Pin(14, mode=Pin.OUT, value=1)
        self.cs = Pin(13, mode=Pin.OUT, value=1)
        self.blk = Pin(12, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)
        pass

    def write_ir(self, ir, ib):
        # print(hex(ir), hex(ib))
        ir_buf = bytearray([0x00, ir])
        ib_buf = bytearray([R61505W_CMD_SET_WDR, ib >> 8, ib & 0xff])
        # ib_buf = bytearray([ib & 0xff, ib >> 8])
        # print("ib_buf:", list(ib_buf))
        self.cs.low()
        self.spi_write8(R61505W_CMD_SET_IR)
        self.spi.write(ir_buf)
        self.cs.high()

        self.cs.low()
        # self.spi.write(bytearray([0x72]))
        self.spi.write(ib_buf)
        self.cs.high()

    def read_ir(self, ir):
        ir_buf = bytearray([0x00, ir])
        result = bytearray(2)
        self.cs.low()
        self.spi_write8(R61505W_CMD_SET_IR)
        self.spi.write(ir_buf)
        self.cs.high()

        self.cs.low()
        self.spi_write8(R61505W_CMD_GET_RDR)
        self.spi.write_readinto(ir_buf, result)
        self.cs.high()
        # print(result)
        return int.from_bytes(result, "big")

    def ir_dump(self):
        for i in range(0, 255):
            print(hex(i), ":", self.read_ir(i))

    def read_id(self):
        return self.read_ir(0x00)

    def init_display(self):
        self.reset()
        time.sleep_ms(50)

        self.write_ir(R61505W_REG_NVM_CTRL4, 0x01)
        time.sleep_ms(2)

        pc3 = self.read_ir(0x12)
        print(hex(pc3))
        self.write_ir(0x12, pc3 | 0x30)
        pc3 = self.read_ir(0x12)
        print(hex(pc3))

        self.write_ir(R61505W_REG_DISP_CTRL1, 0x10)
        print(hex(self.read_ir(R61505W_REG_DISP_CTRL1)))

    def set_window(self, xs, xe, ys, ye):
        pass

    def reset(self):
        self.rst.high()
        time.sleep_us(100)
        self.rst.low()
        time.sleep_us(100)
        self.rst.high()

    def put_pixel(self, x, y, color):
        pass

    def clear(self):
        self.write_ir(R61505W_REG_X_ADDR, 0x00)
        self.write_ir(R61505W_REG_Y_ADDR, 0x00)

        ir = R61505W_REG_MEM_WRITE
        ib_buf = bytearray([R61505W_CMD_SET_WDR, ir >> 8, ir & 0xff])

        self.cs.low()
        self.spi.write(ib_buf)
        for i in range(0, TFT_HOR_RES * TFT_VER_RES):
            self.spi.write(bytearray([0x00, 0x00]))
        self.cs.high()

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = r61505w()
    dev.init_display()

    print("Device code:", hex(dev.read_id()))

    # dev.clear()
    # entry_mode = dev.read_ir(0x03)
    # print(hex(entry_mode))
    # dev.write_ir(0x03, entry_mode | 0x08)
    # entry_mode = dev.read_ir(0x03)
    # print(hex(entry_mode))

    # while True:
    #     dev.blk.on()
    #     time.sleep_ms(50)
    #     dev.blk.off()
    #     time.sleep_ms(50)
    # print("cleaning screen ...")
    # dev.clear()

    # print("drawing test...")

    # for x in range(80):
    #     dev.put_pixel(x, x, 0x56)

    # dev.clear()
    #
    # for x in range(128):
    #     for y in range(128):
    #         dev.put_pixel(x, y, 0xf12c)
    #
    # dev.clear()

    # dev.set_window(0, 127, 0, 127)
    # for x in range(128):
    #     for y in range(128):
    #         dev.write_data(0xfd)
    #         dev.write_data(0x2c)