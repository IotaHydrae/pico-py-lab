import time

from machine import SPI, Pin

SSD1681_PIN_SCL = 18
SSD1681_PIN_SDA = 19
SSD1681_PIN_RES = 15
SSD1681_PIN_DC = 14
SSD1681_PIN_CS = 13
SSD1681_PIN_BUSY = 12


class spi_ifce(object):
    def __init__(self, speed=400000, sck=18, mosi=19, miso=16, csPin=13):
        self.speed = speed
        self.sck = sck
        self.mosi = mosi
        self.miso = miso
        self.csPin = csPin

        self.spi = SPI(0,
                       baudrate=self.speed,
                       sck=Pin(self.sck),
                       mosi=Pin(self.mosi),
                       miso=Pin(self.miso))
        self.cs = Pin(self.csPin, mode=Pin.OUT, value=1)

    def cs_select(self):
        self.cs.value(0)

    def cs_deselect(self):
        self.cs.value(1)

    def surround_cs(self, fun):
        def wrapper(*args, **kwargs):
            self.cs_select()
            rc = fun(*args, **kwargs)
            self.cs_deselect()
            return rc

        return wrapper

    # @surround_cs
    # def read_byte(self):
    #     self.spi.read(1, 0x00)
    #     pass

    # @surround_cs
    def write_byte(self, val):
        val = val.to_bytes(1, 'little')
        self.cs_select()
        self.spi.write(val)
        self.cs_deselect()
        pass


class ssd1681(spi_ifce):

    def __init__(self, sck, mosi, csPin, resPin, dcPin, busyPin):
        self.csPin = csPin
        self.resPin = resPin
        self.dcPin = dcPin
        self.busyPin = busyPin
        super().__init__(csPin=self.csPin)

        self.res = Pin(self.resPin, mode=Pin.OUT, value=1)
        self.dc = Pin(self.dcPin, mode=Pin.OUT, value=0)
        self.busy = Pin(self.busyPin, mode=Pin.IN)

        self.fb = list(range(200 * 25))
        for i in self.fb:
            self.fb[i] = 0xff

    def res_set(self):
        self.res.value(1)

    def res_clr(self):
        self.res.value(0)

    def dc_set(self):
        self.dc.value(1)

    def dc_clr(self):
        self.dc.value(0)

    def dc_cmd(self, fun):
        def wrapper(*args, **kwargs):
            self.dc_clr()
            rc = fun(*args, **kwargs)
            self.dc_set()
            return rc

        return wrapper

    def dc_data(self, fun):
        def wrapper(*args, **kwargs):
            self.dc_set()
            rc = fun(*args, **kwargs)
            self.dc_clr()
            return rc

        return wrapper

    # @dc_cmd
    def write_reg(self, reg):
        # print("reg :", reg)
        self.dc_clr()
        super().write_byte(reg)
        self.dc_set()

    # @dc_data
    def write_data(self, val):
        # print("data :", val)
        self.dc_set()
        super().write_byte(val)
        self.dc_clr()

    def wait_for_busy(self):
        # print("wait for busy...")
        while self.busy.value():
            pass

    def device_init(self):
        # init sequence
        self.res_clr()
        time.sleep_ms(20)
        self.res_set()
        time.sleep_ms(20)
        self.wait_for_busy()

        self.write_reg(0x12)  # Software reset
        self.wait_for_busy()

        self.write_reg(0x01)
        self.write_data(0xC7)
        self.write_data(0x00)
        self.write_data(0x01)

        self.write_reg(0x11)
        self.write_data(0x01)

        self.write_reg(0x44)
        self.write_data(0x00)
        self.write_data(0x18)  # 0x0F -->(15 + 1) * 8 = 128

        self.write_reg(0x45)
        self.write_data(0xC7)  # 0xF9 -->(249 + 1) = 250
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_reg(0x3C)
        self.write_data(0x05)

        self.write_reg(0x18)  # Read built-in temperature sensor
        self.write_data(0x80)

        self.write_reg(0x4E)  # set RAM x address count to 0;
        self.write_data(0x00)
        self.write_data(0x4F)  # set RAM y address count to 0X199;
        self.write_data(0xC7)
        self.write_data(0x00)
        self.wait_for_busy()

    def update(self):
        self.write_reg(0x22)
        self.write_data(0xf7)
        self.write_reg(0x20)
        self.wait_for_busy()

    def flush(self):
        self.write_reg(0x24)
        for i in range(200 * 25):
            self.write_data(self.fb[i])
        self.update()

    def draw_pixel(self, x, y, color):
        if color:
            self.fb[y * 25 + int(x / 8)] &= ~(1 << (7 - x % 8))
        else:
            self.fb[y * 25 + int(x / 8)] |= (1 << (7 - x % 8))
        pass

def main():
    display = ssd1681(
        sck=SSD1681_PIN_SCL,
        mosi=SSD1681_PIN_SDA,
        resPin=SSD1681_PIN_RES,
        dcPin=SSD1681_PIN_DC,
        csPin=SSD1681_PIN_CS,
        busyPin=SSD1681_PIN_BUSY
    )

    display.device_init()

    # display.write_reg(0x24)
    # for i in range(200 * 25):
    #     display.write_data(0x00)
    # display.update()
    #
    # display.write_reg(0x24)
    # for i in range(200 * 25):
    #     display.write_data(0xff)
    # display.update()

    for x in range(50, 100):
        for y in range(50, 100):
            display.draw_pixel(x, y, 1)

    display.flush()

if __name__ == '__main__':
    main()
