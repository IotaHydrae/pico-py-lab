import time

from machine import UART, Pin

"""
Default config for ATGM338H
data bit : 8
stop bit : 1
check bit : none
"""

"""
Format of a NMEA message, take a look at https://www.nmea.org/content/STANDARDS/NMEA_0183_Standard
     $       <address>  {,<value>}  *<checksum>  <CR><LF>
Start flag   
"""

g_nmea_0183_sentences = [
    "AAM",
    "ABK",
    "ABM",
    "ACA",
    "ACF",
    "ACG",
    "ACK",
    "ACM",
    "ACS",
    "ADS",
    "AFB",
    "AGA",
    "AID",
    "AIR",
    "AKD",
    "ALA",
    "ALM",
    "ALR",
    "APB",
    "ASN",
    "BBM",
    "BCG",
    "BCL",
    "BEC",
    "BOD",
    "BWC",
    "BWR",
    "BWW",
    "CEK",
    "COP",
    "CBR",
    "CPC",
    "CPD",
    "CPG",
    "CPN",
    "CPR",
    "CPS",
    "CPT",
    "CUR",
    "DBT",
    "DCN",
    "DCR",
]

g_nmea_0183_sentences_lite = [
    "GGA",
    "GLL",
    "GSA",
    "GSV",
    "RMC",
    "VTG",
    "GST",
    "ZDA",
    "ANT",
    "LPS",
    "DHV",
    "UTC",
]

"""
NMEA 0183 Version 4.11 Sentence talker Identifiers
"""
g_sentence_talker_kv = {'AB': "Independent AIS Base Station",
                        'AD': "Dependent AIS Base Station",
                        'GN': "Global Navigation Satellite System (GNSS)",
                        'GP': "Global Positioning System (GPS)",
                        'BD': "Beidou Satellite System"}


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

    def write_b0yte(self, byte):
        return self.uart.write(byte)

    def read_lines(self) -> list:
        rx_data = bytes()
        lines = []
        while self.uart.any() > 0:
            rx_data += self.uart.readline()

        return rx_data.decode('utf-8').split("\r\n")
        # print(rx_data.decode('utf-8'))
        # print(lines)


atgm338h_message_list = []


class atgm338h_nmea_message(object):

    def __init__(self, message):
        self.kv_list = {}
        pass

    def set_k_v(self, k, v):
        self.kv_list += {k:v}



class atgm338h_nmea_message_GGA(atgm338h_nmea_message):

    def __init__(self, message):
        self.gga_message_body = {}
        pass

    def processor(self):
        # utc_time = word_list[1]  # format: hhmmss.sss
        #
        # lat = word_list[2]  # format: ddmm.mmmm
        #
        # uLat = word_list[3]
        #
        # lon = word_list[4]
        #
        # fs = word_list[5]
        #
        # numSv = word_list[6]
        #
        # HDOP =

"""
Example:
    $GNGGA,,,,,,0,00,25.5,,,,,,*64
    $GNGLL,,,,,,V,M*79
    $GNGSA,A,1,,,,,,,,,,,,,25.5,25.5,25.5,1*01
    $GNGSA,A,1,,,,,,,,,,,,,25.5,25.5,25.5,4*04
    $GPGSV,1,1,00,0*65
    $BDGSV,1,1,00,0*74
    $GNRMC,,V,,,,,,,,,,M,V*34
    $GNVTG,,,,,,,,,M*2D
    $GNZDA,,,,,,*56
    $GPTXT,01,01,01,ANTENNA OPEN*25
"""


class atgm338h(uart_ifce):

    def __init__(self, n_uart: int, baudrate: int, pin_tx: int, pin_rx: int):
        super().__init__(n_uart, baudrate, pin_tx, pin_rx)

        self.init_sequence()

    def init_sequence(self) -> None:
        pass

    def read_nmea_all(self) -> list:
        # print(super().read_lines())
        return super().read_lines()

    def processor(self):
        for message in self.read_nmea_all():
            if message is '':
                # print("skip empty message")
                continue
            # print("Parsing...", message)
            word_list = message.split(",")

            message_id = word_list[0]
            remote_system = message_id[1:3]
            message_type = message_id[3:]

            if message_type in g_nmea_0183_sentences_lite:

            print(remote_system, message_type)
            if remote_system in g_sentence_talker_kv:
                print(g_sentence_talker_kv[remote_system])


def main():
    time.sleep(2)
    atgm338h_dev = atgm338h(0, 9600, 0, 1)
    while True:
        # atgm338h_dev.read_nmea_all()
        atgm338h_dev.processor()
        time.sleep(1)


if __name__ == '__main__':
    main()
