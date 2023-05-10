import time

from machine import Pin, SPI

eink_3in27_lut_vcom_dc = [0x0E, 0x14, 0x01, 0x0A, 0x06, 0x04, 0x0A, 0x0A, 0x0F, 0x03, 0x03, 0x0C, 0x06, 0x0A, 0x00]
eink_3in27_lut_ww = [0x0E, 0x14, 0x01, 0x0A, 0x46, 0x04, 0x8A, 0x4A, 0x0F, 0x83, 0x43, 0x0C, 0x86, 0x0A, 0x04]
eink_3in27_lut_wb = [0x8E, 0x94, 0x01, 0x8A, 0x06, 0x04, 0x8A, 0x4A, 0x0F, 0x83, 0x43, 0x0C, 0x0A, 0x00, 0x04]
eink_3in27_lut_bb = [0x8E, 0x94, 0x01, 0x8A, 0x06, 0x04, 0x8A, 0x4A, 0x0F, 0x83, 0x43, 0x0C, 0x0A, 0x00, 0x04]
eink_3in27_lut_bw = [0x0E, 0x14, 0x01, 0x8A, 0x06, 0x04, 0x8A, 0x4A, 0x0F, 0x83, 0x43, 0x0C, 0x06, 0x4A, 0x04]

EPD_HOR_RES = 300
EPD_VER_RES = 200

class eink_3in27(object):
    def __init__(self):
        self.spi = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11), miso=Pin(8))

        self.busy = Pin(3, mode=Pin.IN)
        self.rst = Pin(6, mode=Pin.OUT, value=1)
        self.dc = Pin(7, mode=Pin.OUT, value=1)
        self.cs = Pin(9, mode=Pin.OUT, value=1)

        self.epd_3in52_flag = 1

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

    def load_reg(self):
        self.write_cmd(0x20)  # vcom
        for i in range(len(eink_3in27_lut_vcom_dc)):
            self.write_data(eink_3in27_lut_vcom_dc[i])

        self.write_cmd(0x21)  # red not use
        for i in range(len(eink_3in27_lut_ww)):
            self.write_data(eink_3in27_lut_ww[i])

        self.write_cmd(0x22)  # bw r
        for i in range(len(eink_3in27_lut_bw)):
            self.write_data(eink_3in27_lut_bw[i])

        self.write_cmd(0x23)  # wb r
        for i in range(len(eink_3in27_lut_wb)):
            self.write_data(eink_3in27_lut_wb[i])

        self.write_cmd(0x24)  # bb b
        for i in range(len(eink_3in27_lut_bb)):
            self.write_data(eink_3in27_lut_bb[i])

    def wait_busy(self):
        self.write_cmd(0x71)
        time.sleep_ms(150)
        while not self.busy.value():
            continue

    def init_display(self):
        self.reset()

        self.write_cmd(0x01);
        self.write_data(0x07);
        self.write_data(0x00);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0x06);
        self.write_data(0x07);
        self.write_data(0x07);
        self.write_data(0x07);

        self.write_cmd(0x04);
        self.wait_busy();

        self.write_cmd(0x00);
        self.write_data(0xCf);
        self.write_cmd(0x50);
        self.write_data(0x37);
        self.write_cmd(0x30);
        self.write_data(0x39);
        self.write_cmd(0x61);
        self.write_data(0xC8);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_cmd(0X82);
        self.write_data(0x0C);

        self.load_reg();

    def turn_on_display(self):
        self.write_cmd(0x12)
        time.sleep_ms(100)
        self.wait_busy()

    def reset(self):
        self.rst.low()
        time.sleep_us(200)
        self.rst.high()

    def fill(self, color: bool):
        pass

    def clear(self):
        self.write_cmd(0x10)
        for i in range(15000):
            self.write_data(0x00);
        self.write_cmd(0x10)
        for i in range(15000):
            self.write_data(0xff);
        pass

    def show_img(self, img):
        self.write_cmd(0x10)
        for i in range(15000):
            # write binary image content
            pass

    def sleep(self):
        self.write_cmd(0x50)
        self.write_data(0x37)
        self.write_cmd(0x02)
        self.write_cmd(0x07)
        self.write_data(0xa5)
        pass


if __name__ == "__main__":
    dev = eink_3in27()
    dev.init_display()
    dev.clear()
    dev.turn_on_display()

    # dev.sleep()
