import time

from machine import UART, Pin

"""
Default config for ATGM338H
data bit : 8
stop bit : 1
check bit : none
"""

"""
NMEA message

$  <address>  {,<value>}  *<checksum>  <CR><LF>
"""

class uart_ifce(object):

    def __init__(self, n_uart=0, baudrate=9600, pin_tx=0, pin_rx=1):
        self.n_uart = n_uart
        self.baudrate = baudrate
        self.pin_tx = pin_tx
        self.pin_rx = pin_rx

        self.uart = UART(self.n_uart,
                         baudrate=self.baudrate,
                         tx=Pin(self.pin_tx),
                         rx=Pin(self.pin_rx))
        pass

    def read_byte(self):
        return self.uart.read(1)

    def write_byte(self, byte):
        return self.uart.write(byte)

    def read_lines(self) -> bytes:
        rx_data = bytes()
        while self.uart.any() > 0:
            rx_data += self.read_byte()
        # return rx_data.decode('utf-8')
        # print(rx_data.decode('utf-8'))
        return rx_data

class atgm338h(uart_ifce):

    def __init__(self, n_uart: int, baudrate: int, pin_tx: int, pin_rx: int):
        super().__init__(n_uart, baudrate, pin_tx, pin_rx)

        self.init_sequence()

    def init_sequence(self) -> None:
        pass

    def read_nmea_all(self) -> str:
        return super().read_lines().decode('utf-8')

def main():
    time.sleep(3)
    atgm338h_dev = atgm338h(0, 9600, 0, 1)
    # uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    while True:
        # rx_data = bytes()
        print(atgm338h_dev.read_nmea_all())
        # while uart0.any() > 0:
        #     rx_data += uart0.read(1)
        #
        # print(rx_data.decode('utf-8'))
        time.sleep(1)
    pass


if __name__ == '__main__':
    main()
