import time

from machine import SPI, Pin

SSD1680_PIN_SCL = 10
SSD1680_PIN_SDA = 11
SSD1680_PIN_RES = 6
SSD1680_PIN_DC = 7
SSD1680_PIN_CS = 9
SSD1680_PIN_BUSY = 3

SSD1680_BLACK = True
SSD1680_WHITE = False

SSD1680_UPDATE_MODE_PART = 0
SSD1680_UPDATE_MODE_FULL = 1


class spi_ifce(object):
    def __init__(self, speed=1000000, sck=10, mosi=11, miso=8, csPin=9):
        self.speed = speed
        self.sck = sck
        self.mosi = mosi
        self.miso = miso
        self.csPin = csPin

        self.spi = SPI(1, baudrate=2000000, sck=Pin(10), mosi=Pin(11), miso=Pin(8))

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


class ssd1680(spi_ifce):

    def __init__(self, sck, mosi, csPin, resPin, dcPin, busyPin):
        self.csPin = csPin
        self.resPin = resPin
        self.dcPin = dcPin
        self.busyPin = busyPin
        super().__init__()

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
        pass
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
        self.write_data(0xF9)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_reg(0x11)
        self.write_data(0x01)

        self.write_reg(0x44)
        self.write_data(0x00)
        self.write_data(0x0F)  # 0x0F -->(15 + 1) * 8 = 128

        self.write_reg(0x45)
        self.write_data(0xF9)  # 0xF9 -->(249 + 1) = 250
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_reg(0x3C)
        self.write_data(0x05)

        self.write_reg(0x21)
        self.write_data(0x00)
        self.write_data(0x80)

        self.write_reg(0x18)  # Read built-in temperature sensor
        self.write_data(0x80)

        self.write_reg(0x4E)  # set RAM x address count to 0;
        self.write_data(0x00)
        self.write_data(0x4F)  # set RAM y address count to 0X199;
        self.write_data(0xF9)
        self.write_data(0x00)
        self.wait_for_busy()

    def update(self, update_mode: int = SSD1680_UPDATE_MODE_FULL):
        self.write_reg(0x22)
        if update_mode == SSD1680_UPDATE_MODE_FULL:
            self.write_data(0xf7)
        elif update_mode == SSD1680_UPDATE_MODE_PART:
            self.write_data(0xff)
        else:
            print("""given update mode is incompatible,
                    using default update mode: SSD1680_UPDATE_MODE_FULL""")
            self.write_data(0xf7)
        self.write_reg(0x20)
        self.wait_for_busy()

    def clear(self):
        self.write_reg(0x24)
        for i in range(200 * 25):
            self.write_data(0xff)
        self.update()

    # TODO: need a logic to decide to use full or part update
    def flush(self):
        self.write_reg(0x24)
        for i in range(200 * 25):
            self.write_data(self.fb[i])
        self.update()

    def draw_pixel(self, x, y, color: bool):
        """
        This function used to draw a single pixel on
        given (x,y) pos with 'color'
        :param x:       pos on x
        :param y:       pos on y
        :param color:   color of this pixel
        :return:        none
        """
        if color:
            self.fb[y * 25 + int(x / 8)] &= ~(1 << (7 - x % 8))
        else:
            self.fb[y * 25 + int(x / 8)] |= (1 << (7 - x % 8))

    def draw_rectangle(self, x1, y1, x2, y2, color: bool):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self.draw_pixel(x, y, color)
        pass


def main():
    display = ssd1680(
        sck=SSD1680_PIN_SCL,
        mosi=SSD1680_PIN_SDA,
        resPin=SSD1680_PIN_RES,
        dcPin=SSD1680_PIN_DC,
        csPin=SSD1680_PIN_CS,
        busyPin=SSD1680_PIN_BUSY
    )

    display.device_init()

    display.write_reg(0x24)
    for i in range(200 * 25):
        display.write_data(0x00)
    display.update()

    display.write_reg(0x24)
    for i in range(200 * 25):
        display.write_data(0xff)
    display.update()

    # for x in range(50, 100):
    #     for y in range(50, 100):
    #         display.draw_pixel(x, y, 1)
    #
    # display.flush()


if __name__ == '__main__':
    main()
