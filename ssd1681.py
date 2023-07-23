import time

from machine import SPI, Pin

SSD1681_PIN_SCL = 18
SSD1681_PIN_SDA = 19
SSD1681_PIN_RES = 15
SSD1681_PIN_DC = 14
SSD1681_PIN_CS = 13
SSD1681_PIN_BUSY = 12

SSD1681_BLACK = True
SSD1681_WHITE = False

SSD1681_UPDATE_MODE_PART = 0
SSD1681_UPDATE_MODE_FULL = 1

class spi_ifce(object):
    def __init__(self, speed=50000000, sck=10, mosi=11, miso=8, csPin=9):
        self.spi = SPI(0, baudrate=50000000, sck=Pin(18), mosi=Pin(19))
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        self.dc = Pin(14, mode=Pin.OUT, value=1)
        self.cs = Pin(13, mode=Pin.OUT, value=1)
        self.busy = Pin(12, mode=Pin.OUT, value=1)
        
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
        super().__init__()

        self.res = Pin(self.resPin, mode=Pin.OUT, value=1)
        self.dc = Pin(self.dcPin, mode=Pin.OUT, value=0)
        self.busy = Pin(self.busyPin, mode=Pin.IN)

        self.fb = list(range(200 * 25))
        self.old_fb = list(range(200 * 25))
        for i in self.fb:
            self.fb[i] = 0xff

        self.refresh_count = 0
        self.update_func = None

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
    def write_cmd(self, reg):
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

    def write_reg(self, *opts):
        reg = opts[0]
        print("reg: ", hex(reg))
        self.write_cmd(reg)

        if len(opts) == 1:
            return

        opts = opts[1:]
        for val in opts:
            print("val: ", hex(val))
            self.write_data(val)

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

        self.write_cmd(0x12)  # Software reset
        self.wait_for_busy()

        self.write_cmd(0x01)
        self.write_data(0xC7)
        self.write_data(0x00)
        self.write_data(0x01)

        self.write_cmd(0x11)
        self.write_data(0x01)

        self.write_cmd(0x44)
        self.write_data(0x00)
        self.write_data(0x18)  # 0x0F -->(15 + 1) * 8 = 128

        self.write_cmd(0x45)
        self.write_data(0xC7)  # 0xF9 -->(249 + 1) = 250
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x3C)
        self.write_data(0x05)

        self.write_cmd(0x18)  # Read built-in temperature sensor
        self.write_data(0x80)

        self.write_cmd(0x4E)  # set RAM x address count to 0;
        self.write_data(0x00)
        self.write_data(0x4F)  # set RAM y address count to 0X199;
        self.write_data(0xC7)
        self.write_data(0x00)
        self.wait_for_busy()

    def set_window(self, xs, ys, xe, ye):
        self.write_cmd(0x44)
        self.write_data(xs & 0xff)
        self.write_data(xe & 0xff)

        self.write_cmd(0x45)
        self.write_data(ys & 0xff)
        self.write_data((ys >> 8) & 0xff)
        self.write_data(ye & 0xff)
        self.write_data((ye >> 8) & 0xff)

    def set_cursor(self, x, y):
        self.write_cmd(0x4e)
        self.write_data(x & 0xff)
        self.write_cmd(0x4f)
        self.write_data(y & 0xff)
        self.write_data((y >> 8) & 0xff)

    def deep_sleep(self):
        self.write_cmd(0x10)
        self.write_data(0x01)
        time.sleep_ms(100)


    def update_part(self):
        self.write_cmd(0x22)
        self.write_data(0xff)
        self.write_cmd(0x20)
        self.wait_for_busy()
        return 0

    def update_full(self):
        self.write_cmd(0x22)
        self.write_data(0xf7)
        self.write_cmd(0x20)
        self.wait_for_busy()
        return 0

    def update_fast(self):
        self.write_cmd(0x22)
        self.write_data(0xc7)
        self.write_cmd(0x20)
        self.wait_for_busy()
        return 0

    def update(self, update_mode: int = SSD1681_UPDATE_MODE_FULL):
        self.write_cmd(0x22)
        if update_mode == SSD1681_UPDATE_MODE_FULL:
            self.write_data(0xf7)
        elif update_mode == SSD1681_UPDATE_MODE_PART:
            self.write_data(0xff)
        else:
            print("""given update mode is incompatible,
                    using default update mode: SSD1681_UPDATE_MODE_FULL""")
            self.write_data(0xf7)
        self.write_cmd(0x20)
        self.wait_for_busy()

    def reset(self):
        self.res_set()
        self.res_clr()
        time.sleep_ms(2)
        self.res_set()

    def clear(self):
        self.write_cmd(0x24)
        for i in range(200 * 25):
            self.write_data(0xff)
        self.update(update_mode=SSD1681_UPDATE_MODE_PART)

    def flush(self):
        self.update_func = self.update_full
        diff = 0

        self.reset()
        self.write_cmd(0x3c)
        self.write_data(0x80)

        self.write_cmd(0x44)
        self.write_data(0x00)
        self.write_data(0x18)

        self.write_cmd(0x45)
        self.write_data(0xc7)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x24)
        for i in range(200 * 25):
            if self.fb[i] != self.old_fb[i]:
                diff+=1
            self.write_data(self.fb[i])

        if diff == 0:
            return

        if diff < (200 * 25 / 3):
            self.update_func = self.update_part
        else:
            self.update_func = self.update_full

        self.refresh_count+=1

        if (self.refresh_count % 5) == 0:
            self.update_func = self.update_full

        self.update_func()

        for i in range(200 * 25):
            self.old_fb[i] = self.fb[i]

    def draw_pixel(self, x, y, color: bool):
        """
        This function used to draw a single pixel on
        given (x,y) pos with 'color'
        :param x:       pos on x
        :param y:       pos on y
        :param color:   color of this pixel
        :return:        none
        """
        if x < 0 or x >= 200 or y < 0 or y >= 200:
            return

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
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    display = ssd1681(
        sck=SSD1681_PIN_SCL,
        mosi=SSD1681_PIN_SDA,
        resPin=SSD1681_PIN_RES,
        dcPin=SSD1681_PIN_DC,
        csPin=SSD1681_PIN_CS,
        busyPin=SSD1681_PIN_BUSY
    )

    display.device_init()

    display.write_cmd(0x24)
    for i in range(200 * 25):
        display.write_data(0x00)
    # display.update(update_mode=SSD1681_UPDATE_MODE_PART)
    display.update_part()

    display.write_cmd(0x24)
    for i in range(200 * 25):
        display.write_data(0xff)
    # display.update(update_mode=SSD1681_UPDATE_MODE_PART)
    display.update_part()

    for x in range(200):
            display.draw_pixel(x, x - 1, 1)
            display.draw_pixel(x, x, 1)
            display.draw_pixel(x, x + 1, 1)
    display.flush()

    display.draw_rectangle(0, 0, 50, 50, SSD1681_BLACK)
    display.draw_rectangle(50, 50, 100, 100, SSD1681_BLACK)
    display.draw_rectangle(100, 100, 150, 150, SSD1681_BLACK)
    display.draw_rectangle(150, 150, 200, 200, SSD1681_BLACK)
    display.flush()

    display.draw_rectangle(100, 0, 150, 50, SSD1681_BLACK)
    display.draw_rectangle(150, 50, 200, 100, SSD1681_BLACK)
    display.flush()

    display.draw_rectangle(0, 100, 50, 150, SSD1681_BLACK)
    display.draw_rectangle(50, 150, 100, 200, SSD1681_BLACK)

    display.flush()


if __name__ == '__main__':
    main()
