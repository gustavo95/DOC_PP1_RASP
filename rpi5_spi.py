import gpiod
import time

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

    def close_connection(self):
        self.__line_mosi.release()
        self.__line_miso.release()
        self.__line_sck.release()
        self.__line_ss.release()

    def exange_data(self, byte_out):
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

    def set_period(self, time):
        self.__SCK_PERIOD = time

def sendbyte(spi, byte_to_send):
    time.sleep(0.01)
    received = spi.exange_data(byte_to_send)
    print("Byte enviado:  {:08b}".format(byte_to_send), "Byte recebido: {:08b}".format(received))

def main():
    spi = RPi5SPI()
    spi.set_period(0.005)
    print("Sending type")
    sendbyte(spi, 0b00000001)
    print("Sending size")
    sendbyte(spi, 0b00000000)
    sendbyte(spi, 0b00000000)
    sendbyte(spi, 0b00000100)
    print("Sending data")
    sendbyte(spi, 0b11111111)
    sendbyte(spi, 0b01010101)
    sendbyte(spi, 0b00001111)
    sendbyte(spi, 0b10000001)
    sendbyte(spi, 0b00000000)
    spi.close_connection()

if __name__ == "__main__":
    main()