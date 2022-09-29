from machine import Pin, I2C


class i2c_interface(object):
    def __init__(self, ifce=0, scl=5, sda=4, freq=100000):
        self.ifce = ifce
        self.scl = scl
        self.sda = sda
        self.freq = freq

        self.i2c = I2C(self.ifce, scl=Pin(self.scl),
                       sda=Pin(self.sda), freq=self.freq);

    def write_byte_data(self, addr, byte, data):
        self.i2c.writeto_mem(addr, byte, data)

    def write_byte(self, addr, byte):
        self.i2c.writeto(addr, byte)

    def read_byte_data(self, addr, byte):
        return self.i2c.readfrom_mem(addr, 1, 1)

    def read_byte(self, addr):
        return self.i2c.readfrom(addr, 1)

    def i2c_scan(self):
        return self.i2c.scan()


class ds1321(i2c_interface):
    def __init__(self, ifce, dev_addr, scl, sda, freq):
        self.dev_addr = dev_addr
        print("ds1321 dev addr :", self.dev_addr)

        super().__init__(ifce, scl, sda, freq)


class at24c02(i2c_interface):
    def __init__(self, ifce, dev_addr, scl, sda, freq):
        self.dev_addr = dev_addr
        print("at24c02 dev addr :", self.dev_addr)

        super().__init__(ifce, scl, sda, freq)

    def read_addr(self, reg_addr):
        return super().read_byte_data(self.dev_addr, reg_addr)

    def write_addr_byte(self, reg_addr, data):
        print(data)
        print(data.to_bytes(1, 'little'))
        # print(str(data).encode())
        return super().write_byte_data(self.dev_addr, reg_addr, data.to_bytes(1, 'little'))
        pass


def main():
    print("Hello World!")
    # val = 0x12
    # print(val.to_bytes(1, 'little'))
    ds1321_dev = ds1321(0, 104, 5, 4, 100000)
    print(ds1321_dev.i2c_scan())

    at24c02_dev = at24c02(0, 87, 5, 4, 100000)
    at24c02_dev.write_addr_byte(0, 0x12)
    print(at24c02_dev.read_addr(0))

    pass


if __name__ == "__main__":
    main()
