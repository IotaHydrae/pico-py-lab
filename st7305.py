import time

import machine
from machine import Pin, SPI

TFT_HOR_RES = 200   # around to 216 bits in a row actually
TFT_VER_RES = 200

OFFSET_X = 0
OFFSET_Y = 0

g_tft_buf = [0x0] * int(25 * 200)

class st7305(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=5000000, sck=Pin(18), mosi=Pin(19))
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        self.dc = Pin(14, mode=Pin.OUT, value=1)
        self.cs = Pin(13, mode=Pin.OUT, value=1)
        self.blk = Pin(12, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)

    def write_cmd(self, cmd):
        self.dc.low()
        self.cs.low()
        self.spi.write(bytearray([cmd]))
        self.cs.high()
        # self.spi.write(bytearray([cmd]))

    def write_data(self, data):
        self.dc.high()
        self.cs.low()
        self.spi.write(bytearray([data]))
        self.cs.high()
        time.sleep_us(200)
        # self.spi.write(bytearray([data]))

    def write_data_buffered(self, buf):
        self.dc.high()
        # self.cs.low()
        for val in buf:
            self.spi_write8(val)
        # self.cs.high()

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

    def init_display(self):
        # ST7305
        self.write_cmd(0xD6) #NVM Load Control
        self.write_data(0X17)
        self.write_data(0X02)

        self.write_cmd(0xD1) #Booster Enable
        self.write_data(0X01)

        self.write_cmd(0xC0) #Gate Voltage Setting
        self.write_data(0X08) #VGH 00:8V  04:10V  08:12V   0E:15V
        self.write_data(0X02) #VGL 00:-5V   04:-7V   0A:-10V


        # VLC=3.6V (12/-5)(delta Vp=0.6V)
        self.write_cmd(0xC1) #VSHP Setting (4.8V)
        self.write_data(0X19) #VSHP1
        self.write_data(0X19) #VSHP2
        self.write_data(0X19) #VSHP3
        self.write_data(0X19) #VSHP4

        self.write_cmd(0xC2) #VSLP Setting (0.98V)
        self.write_data(0X31) #VSLP1
        self.write_data(0X31) #VSLP2
        self.write_data(0X31) #VSLP3
        self.write_data(0X31) #VSLP4

        self.write_cmd(0xC4) #VSHN Setting (-3.6V)
        self.write_data(0X19) #VSHN1
        self.write_data(0X19) #VSHN2
        self.write_data(0X19) #VSHN3
        self.write_data(0X19) #VSHN4

        self.write_cmd(0xC5) #VSLN Setting (0.22V)
        self.write_data(0X27) #VSLN1
        self.write_data(0X27) #VSLN2
        self.write_data(0X27) #VSLN3
        self.write_data(0X27) #VSLN4

        self.write_cmd(0xD8) #HPM=32Hz
        self.write_data(0XA6) #~32Hz
        self.write_data(0XE9) #~1Hz

        # self.write_cmd(0xD8) #HPM=51Hz
        # self.write_data(0X80) #~51Hz
        # self.write_data(0XE9) #~1Hz

        # See manual page 76 FRCTRL(B2h) for more info
        self.write_cmd(0xB2) #Frame Rate Control
        self.write_data(0X02) #HPM=16hz  LPM=1hz

        self.write_cmd(0xB3) #Update Period Gate EQ Control in HPM
        self.write_data(0XE5)
        self.write_data(0XF6)
        self.write_data(0X05) #HPM EQ Control
        self.write_data(0X46)
        self.write_data(0X77)
        self.write_data(0X77)
        self.write_data(0X77)
        self.write_data(0X77)
        self.write_data(0X76)
        self.write_data(0X45)

        self.write_cmd(0xB4) #Update Period Gate EQ Control in LPM
        self.write_data(0X05) #LPM EQ Control
        self.write_data(0X46)
        self.write_data(0X77)
        self.write_data(0X77)
        self.write_data(0X77)
        self.write_data(0X77)
        self.write_data(0X76)
        self.write_data(0X45)

        self.write_cmd(0x62) #Gate Timing Control
        self.write_data(0X32)
        self.write_data(0X03)
        self.write_data(0X1F)


        self.write_cmd(0xB7) #Source EQ Enable
        self.write_data(0X13)

        self.write_cmd(0xB0) #Gate Line Setting
        self.write_data(0X32) #200 line

        self.write_cmd(0x11) #Sleep out
        time.sleep_ms(120)

        self.write_cmd(0xC9) #Source Voltage Select
        self.write_data(0X00) #VSHP1 VSLP1  VSHN1  VSLN1

        self.write_cmd(0x36) #Memory Data Access Control
        self.write_data(0X48) #MX=1  DO=1 	#48

        self.write_cmd(0x3A) #Data Format Select
        self.write_data(0x11) #10:4write for 24bit  11: 3write for 24bit

        self.write_cmd(0xB9) #Gamma Mode Setting
        self.write_data(0X20) #20: Mono 00:4GS

        self.write_cmd(0xB8) #Panel Setting
        self.write_data(0X29) # Panel Setting Frame inversion  09:column 29:dot_1-Frame 25:dot_1-Line

        #WRITE RAM 200*200
        self.write_cmd(0x2A) #Column Address Setting
        self.write_data(0x16)#10
        self.write_data(0x26) #38

        self.write_cmd(0x2B) #Row Address Setting
        self.write_data(0X00)
        self.write_data(0X63) #63

        # self.write_cmd(0x72) #de-stress off
        # self.write_data(0X13)

        self.write_cmd(0x35) #TE
        self.write_data(0X00) #

        self.write_cmd(0xD0) #Auto power dowb
        self.write_data(0XFF) #

        self.write_cmd(0x38) #HPM
        # self.write_cmd(0x39) #LPM

        self.write_cmd(0x29) #DISPLAY ON

    def set_window(self, xs, xe, ys, ye):
        # offset_x = OFFSET_X
        # offset_y = OFFSET_Y

        # xs = xs + offset_x
        # xe = xe + offset_x
        # ys = ys + offset_y
        # ye = ye + offset_y
        self.write_cmd(0x2A) #Column Address Setting
        self.write_data(0x16)
        self.write_data(0x26)

        self.write_cmd(0x2B) #Row Address Setting
        self.write_data(0X00)
        self.write_data(0X63) #99, Max 159

        self.write_cmd(0x2C)   #write image data

    def reset(self):
        self.rst.high()
        time.sleep_us(100)
        self.rst.low()
        time.sleep_us(100)
        self.rst.high()

    def clear(self):
        self.write_cmd(0x3A)  # Data Format Select
        self.write_data(0x11) # 10:4write for 24bit ; 11: 3write for 24bit

        self.set_window(0, 0, 199, 199)
        for i in range(100):
            for j in range(8):
                self.write_data(0x00)
                self.write_data(0x00)
                self.write_data(0x00)
                self.write_data(0x00)
                self.write_data(0x00)
                self.write_data(0x00)
            
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x00)


    def disp_test(self):
        self.write_cmd(0x3A)  # Data Format Select
        self.write_data(0x11) # 10:4write for 24bit ; 11: 3write for 24bit
        
        self.set_window(0, 0, 199, 199)
        for i in range(100):
            if i % 2 == 0:
                for j in range(8):
                    self.write_data(0x00)
                    self.write_data(0x00)
                    self.write_data(0x00)
                    self.write_data(0xff)
                    self.write_data(0xff)
                    self.write_data(0xff)
                self.write_data(0x00)
                self.write_data(0x00)
                self.write_data(0x00)
            else:
                for j in range(8):
                    self.write_data(0xff)
                    self.write_data(0xff)
                    self.write_data(0xff)
                    self.write_data(0x00)
                    self.write_data(0x00)
                    self.write_data(0x00)
                self.write_data(0xff)
                self.write_data(0xff)
                self.write_data(0xff)

    def put_pixel(self, x, y, color):
        ca_slice = int(x / 4)
        addr = int(y / 2) * 48 + ca_slice
        print(x, ca_slice, addr)
        if y % 2 != 0:
            g_tft_buf[addr] |= (0x80 >> (2 * (x % 4) - 2))
        else:
            # TODO: add even rows buffer drawing
            pass

    def flush(self):
        self.write_cmd(0x3A)  # Data Format Select
        self.write_data(0x11) # 10:4write for 24bit ; 11: 3write for 24bit
        self.set_window(0, 0, 199, 199)
        
        for i in range(100):
            self.write_data(0x00) # dummy pixels, left margin
            self.write_data(g_tft_buf[i * 48])
            self.write_data(g_tft_buf[i * 48 + 1])
            
            # TODO: data overflowed
            for j in range(48):
                self.write_data(g_tft_buf[i * 48 + 2 + j])

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    print(len(g_tft_buf))

    dev = st7305()
    dev.init_display()

    print("cleaning screen ...")
    # dev.clear()
    # dev.disp_test()
    
    dev.clear()
    for x in range(200):
        dev.put_pixel(x + 0, x + 0, 1)

    print("flushing...")
    dev.flush()
    print("done.")