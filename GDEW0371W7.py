import time

import machine
from machine import Pin, SPI

GDEW0371W7_lut_vcom_dc = [0x00, 0x0A ,0x00 ,0x00 ,0x00 ,0x01,
0x60  ,0x14 ,0x14 ,0x00 ,0x00 ,0x01,
0x00  ,0x14 ,0x00 ,0x00 ,0x00 ,0x01,
0x00  ,0x13 ,0x0A ,0x01 ,0x00 ,0x01,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00]

GDEW0371W7_lut_ww = [0x40  ,0x0A ,0x00 ,0x00 ,0x00 ,0x01,
0x90  ,0x14 ,0x14 ,0x00 ,0x00 ,0x01,
0x10  ,0x14 ,0x0A ,0x00 ,0x00 ,0x01,
0xA0  ,0x13 ,0x01 ,0x00 ,0x00 ,0x01,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00]

GDEW0371W7_lut_bw = [0x40  ,0x0A ,0x00 ,0x00 ,0x00 ,0x01,
0x90  ,0x14 ,0x14 ,0x00 ,0x00 ,0x01,
0x00  ,0x14 ,0x0A ,0x00 ,0x00 ,0x01,
0x99  ,0x0C ,0x01 ,0x03 ,0x04 ,0x01,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00]

GDEW0371W7_lut_wb = [0x40  ,0x0A ,0x00 ,0x00 ,0x00 ,0x01,
0x90  ,0x14 ,0x14 ,0x00 ,0x00 ,0x01,
0x00  ,0x14 ,0x0A ,0x00 ,0x00 ,0x01,
0x99  ,0x0B ,0x04 ,0x04 ,0x01 ,0x01,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00]

GDEW0371W7_lut_bb = [0x80  ,0x0A ,0x00 ,0x00 ,0x00 ,0x01,
0x90  ,0x14 ,0x14 ,0x00 ,0x00 ,0x01,
0x20  ,0x14 ,0x0A ,0x00 ,0x00 ,0x01,
0x50  ,0x13 ,0x01 ,0x00 ,0x00 ,0x01,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00,
0x00  ,0x00 ,0x00 ,0x00 ,0x00 ,0x00]

EPD_HOR_RES = 300
EPD_VER_RES = 200


# g_tx_buf = [0xff]*4096

class GDEW0371W7(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=8000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

        self.busy = Pin(12, mode=Pin.IN)
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        self.dc = Pin(14, mode=Pin.OUT, value=1)
        self.cs = Pin(13, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)
        pass

    def write_cmd(self, cmd):
        self.dc.low()
        self.cs.low()
        self.spi_write8(cmd)
        self.cs.high()
        pass

    def write_data(self, data):
        self.dc.high()
        self.cs.low()
        self.spi_write8(data)
        self.cs.high()
        pass

    def write_data_buffered(self, buf):
        self.dc.high()
        self.cs.low()
        for val in buf:
            self.spi_write8(val)
        self.cs.high()

    def write_reg(self, *opts):
        reg = opts[0]
        # print("reg: ", reg)
        self.write_cmd(reg)

        if len(opts) == 1:
            return

        opts = opts[1:]
        for val in opts:
            # print("val: ", val)
            self.write_data(val)

    def load_reg(self):
        self.write_reg(0x20)  # vcom
        # for i in range(len(GDEW0371W7_lut_vcom_dc)):
        #     self.write_data(GDEW0371W7_lut_vcom_dc[i])
        self.write_data_buffered(GDEW0371W7_lut_vcom_dc)

        self.write_reg(0x21)  # red not use
        # for i in range(len(GDEW0371W7_lut_ww)):
        #     self.write_data(GDEW0371W7_lut_ww[i])
        self.write_data_buffered(GDEW0371W7_lut_ww)

        self.write_reg(0x22)  # bw r
        # for i in range(len(GDEW0371W7_lut_bw)):
        #     self.write_data(GDEW0371W7_lut_bw[i])
        self.write_data_buffered(GDEW0371W7_lut_bw)

        self.write_reg(0x23)  # wb r
        # for i in range(len(GDEW0371W7_lut_wb)):
        #     self.write_data(GDEW0371W7_lut_wb[i])
        self.write_data_buffered(GDEW0371W7_lut_wb)

        self.write_reg(0x24)  # bb b
        # for i in range(len(GDEW0371W7_lut_bb)):
        #     self.write_data(GDEW0371W7_lut_bb[i])
        self.write_data_buffered(GDEW0371W7_lut_bb)
        
        self.write_reg(0x25)
        self.write_data_buffered(GDEW0371W7_lut_ww)

    def wait_busy(self):
        self.write_reg(0x71)
        while not self.busy.value():
            continue

    def init_display(self):
        self.reset()

        self.write_reg(0x06, 0x17, 0x17, 0x1d)
        
        self.write_reg(0x04)
        self.wait_busy()
        
        self.write_reg(0x00, 0x1f)
        self.write_reg(0x61, 0xf0, 0x01, 0xa0)
        self.write_reg(0x50, 0x23, 0x07)
        
        # self.load_reg()

    def init_display_4gray(self):
        self.reset()
        self.write_reg(0x01, 0x07, 0x07, 0x3f, 0x3f)
        self.write_reg(0x06, 0x17, 0x17, 0x1d)
        
        self.write_reg(0x04)
        self.wait_busy()
        
        self.write_reg(0x00, 0x3f)
        self.write_reg(0x30, 0x04)
        self.write_reg(0x61, 0xf0, 0x01, 0xa0)
        self.write_reg(0x82, 0x08)
        self.write_reg(0x50, 0x11, 0x07)
        

    def display_clean(self):
        self.write_cmd(0x10)
        for i in range(12480):
            self.write_data(0xff)
        self.write_cmd(0x13)
        for i in range(12480):
            self.write_data(0xff)

    def turn_on_display(self):
        self.write_reg(0x12)
        time.sleep_us(250)
        self.wait_busy()

    def reset(self):
        self.rst.low()
        time.sleep_us(200)
        self.rst.high()

    def sleep(self):
        self.write_reg(0x50, 0xf7)
        self.write_reg(0x02)
        self.wait_busy()
        self.write_reg(0x07, 0xA5)


    def clear(self):
        self.write_reg(0x10)
        for i in range(15000):
            self.write_data(0x0)
        self.write_reg(0x10)
        for i in range(15000):
            self.write_data(0xff)
        pass

    def pic_4bit(self):
        self.write_cmd(0x10)
        for i in range(3120):
            self.write_data(0xff)
        for i in range(3120):
            self.write_data(0xff)
        for i in range(3120):
            self.write_data(0x00)
        for i in range(3120):
            self.write_data(0x00)
        self.write_cmd(0x13)
        for i in range(3120):
            self.write_data(0xff)
        for i in range(3120):
            self.write_data(0x00)
        for i in range(3120):
            self.write_data(0xff)
        for i in range(3120):
            self.write_data(0x00)
            
        self.load_reg()
        self.write_cmd(0x12)
        time.sleep_us(250)
        self.wait_busy()

    def sleep(self):
        self.write_reg(0x50, 0x37)
        self.write_reg(0x02)
        self.write_reg(0x07, 0xa5)
        pass


if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = GDEW0371W7()
    
    dev.init_display()
    dev.display_clean()
    dev.turn_on_display()
    dev.sleep()
    
    dev.init_display_4gray()
    dev.pic_4bit()
    dev.sleep()

    dev.init_display()
    dev.display_clean()
    dev.turn_on_display()
    dev.sleep()
    
