import time

from machine import UART, Pin


class uart_ifce(UART):

    def __init__(self, n_uart=0, baudrate=9600, pin_tx=0, pin_rx=1):
        self.uart = UART(n_uart, baudrate=baudrate, tx=Pin(pin_tx), rx=Pin(pin_rx))
        pass

    def readlines(self) -> str:
        rx_data = bytes()
        while self.uart.any() > 0:
            rx_data += self.uart.read(1)
        return rx_data.decode('utf-8')


class atgm338h(uart_ifce):

    def __init__(self, n_uart: int, baudrate: int, pin_tx: int, pin_rx: int):

        super().__init__(n_uart, baudrate, pin_tx, pin_rx)

        self.init_sequence()

    def init_sequence(self) -> None:
        pass


def main():
    atgm338h_dev = atgm338h(0, 9600, 0, 1)

    while True:
        print(atgm338h_dev.readlines())
        time.sleep(1)
    pass


if __name__ == '__main__':
    main()
