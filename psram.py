import time
from machine import Pin, SPI

class psram(object):
    def __init__(self, cs=13):
        self.spi = SPI(1, baudrate=10_000_000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
        self.cs = Pin(cs, mode=Pin.OUT, value=1)
        self.eid = bytearray(6)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))

    def read_id(self):
        rxdata = bytearray(8)

        self.cs(0)
        self.spi_write8(0x9f)
        self.spi_write8(0xff)
        self.spi_write8(0xff)
        self.spi_write8(0xff)
        self.spi.readinto(rxdata, 0xff)
        self.cs(1)

        self.eid = rxdata[2:]

        print("MFID : ", hex(rxdata[0]))
        print("KGD  :", hex(rxdata[1]))
        print("EID  : ", end="")
        for byte in self.eid:
            print(hex(byte), end=" ")
        print()

    def read(self, addr, buf : bytearray, length):
        if length > len(buf):
            print("ERR: out of bound!")
        self.cs(0)
        self.spi_write8(0x03)
        self.spi_write8((addr >> 16) & 0xff)
        self.spi_write8((addr >> 8) & 0xff)
        self.spi_write8((addr >> 0) & 0xff)
        self.spi.readinto(buf, 0xff)
        self.cs(1)

    def write(self, addr, buf, length):
        if length > len(buf):
            print("ERR: out of bound!")

        self.cs(0)
        self.spi_write8(0x02)
        self.spi_write8((addr >> 16) & 0xff)
        self.spi_write8((addr >> 8) & 0xff)
        self.spi_write8((addr >> 0) & 0xff)
        for i in range(length):
            self.spi_write8(buf[i])
        self.cs(1)

if __name__ == "__main__":
    dev = psram(cs=13)

    print("PSRAM read/write Test.")

    test_data = [0x12, 0x34, 0x56, 0x78]
    read_out = bytearray(4)

    dev.read_id()

    print("writing psram...")
    dev.write(0x12, test_data, len(test_data))
    print("reading psram...")
    dev.read(0x12, read_out, len(read_out))

    for i in read_out:
        print(hex(i))