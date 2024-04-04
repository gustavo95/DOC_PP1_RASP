import time
import numpy as np
from rpi5_spi import RPi5SPI

class CommunicationController:

    def __init__(self) -> None:
        self.spi = RPi5SPI()
        self.spi.set_period(0.005)

    def sendbyte(self, byte_to_send):
        time.sleep(0.01)
        received = self.spi.exange_data(byte_to_send)
        print("Byte enviado:  {:08b}".format(byte_to_send), "Byte recebido: {:08b}".format(received))

    def test(self):
        print("Sending type")
        self.sendbyte(1)
        print("Sending size")
        self.sendbyte(0b00000000)
        self.sendbyte(0b00000010)
        self.sendbyte(0b00000000)
        self.sendbyte(0b00000010)
        print("Sending data")
        self.sendbyte(0b11111111)
        self.sendbyte(0b01010101)
        self.sendbyte(0b00001111)
        self.sendbyte(0b10000001)
        self.sendbyte(0b00000000)

    def send_img(self, img) -> None:

        self.sendbyte(np.uint8(1))

        height, width = img.shape[0:2]

        height_bytes = self.toUnint8(height, 2)
        width_bytes = self.toUnint8(width, 2)

        self.sendbyte(height_bytes[0])
        self.sendbyte(height_bytes[1])
        self.sendbyte(width_bytes[0])
        self.sendbyte(width_bytes[1])

        for y in range(height):
            for x in range(width):
                pixel = img[y, x]
                print(pixel)
                self.sendbyte(pixel)
        
        self.sendbyte(0)


    def toUnint8(self, data, num_bytes) -> np.uint8:
        data_bytes = data.to_bytes(num_bytes, "big")
        return np.frombuffer(data_bytes, dtype=np.uint8)


    def close_communication(self) -> None:
        print("Closing connection")
        self.spi.close_connection()

        

