import gpiod
import time
import numpy as np

class RPi5SPI:

    __MOSI_PIN = 10
    __MISO_PIN = 9
    __SCK_PIN = 11
    __SS_PIN = 22
    __CHIP_NAME = "gpiochip4"

    __SCK_PERIOD = 1

    def __init__(self) -> None:
        self.chip = gpiod.Chip(self.__CHIP_NAME)

        self.__line_mosi = self.chip.get_line(self.__MOSI_PIN)
        self.__line_miso = self.chip.get_line(self.__MISO_PIN)
        self.__line_sck = self.chip.get_line(self.__SCK_PIN)
        self.__line_ss = self.chip.get_line(self.__SS_PIN)

        self.__line_mosi.request(consumer="spi_mosi", type=gpiod.LINE_REQ_DIR_OUT)
        self.__line_miso.request(consumer="spi_miso", type=gpiod.LINE_REQ_DIR_IN)
        self.__line_sck.request(consumer="spi_sck", type=gpiod.LINE_REQ_DIR_OUT)
        self.__line_ss.request(consumer="spi_ss", type=gpiod.LINE_REQ_DIR_OUT)

    def close_connection(self) -> None:
        self.__line_mosi.release()
        self.__line_miso.release()
        self.__line_sck.release()
        self.__line_ss.release()

    def exange_data(self, byte_out : np.uint8) -> int:
        byte_in = 0
        
        self.__line_ss.set_value(0)
        
        for i in range(8):
            self.__line_mosi.set_value((byte_out >> (7 - i)) & 0x01)
            time.sleep(self.__SCK_PERIOD/4)
            self.__line_sck.set_value(1)
            time.sleep(self.__SCK_PERIOD/4)
            bit = self.__line_miso.get_value()
            # print(bit)
            byte_in = (byte_in << 1) | bit
            self.__line_sck.set_value(0)
            time.sleep(self.__SCK_PERIOD/2)
            
        self.__line_ss.set_value(1)

        return byte_in

    def set_period(self, time) -> None:
        self.__SCK_PERIOD = time