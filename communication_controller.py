import time
import numpy as np
from rpi5_spi import RPi5SPI

class CommunicationController:

    def __init__(self) -> None:
        self.spi = RPi5SPI()
        self.frequency = 12000000
        self.delay_time = 1/self.frequency
        self.spi.set_frequency(self.frequency)

    def sendbyte(self, byte_to_send):
        # time.sleep(self.delay_time)
        received = self.spi.exange_data(byte_to_send)
        print("Byte enviado:  {:08b}".format(byte_to_send), "Byte recebido: {:08b}".format(received))
        return received

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

        print(width, height)

        height_bytes = self.toUnint8(height, 2)
        width_bytes = self.toUnint8(width, 2)

        self.sendbyte(height_bytes[0])
        self.sendbyte(height_bytes[1])
        self.sendbyte(width_bytes[0])
        self.sendbyte(width_bytes[1])

        initial_time = time.time()
        for y in range(height):
            for x in range(width):
                pixel = img[y, x]
                # print(y, x, pixel)
                self.sendbyte(pixel)
                time.sleep(1)
        self.sendbyte(0)

        send_time = time.time() - initial_time
        print(f"Time to send image: {send_time}")

    def recive_img(self):
        self.sendbyte(np.uint8(1))

        new_img = np.zeros((120, 160), dtype=np.uint8)
        x = 0
        y = 0

        time.sleep(1)

        for i in range(19200):
            pixel = self.sendbyte(0)
            new_img[y, x] = pixel
            x += 1
            if(x >= 160):
                y += 1
                x = 0
                if (y >= 120):
                    break
            time.sleep(1)
        return new_img


    def toUnint8(self, data, num_bytes) -> np.uint8:
        data_bytes = data.to_bytes(num_bytes, "big")
        return np.frombuffer(data_bytes, dtype=np.uint8)


    def close_communication(self) -> None:
        print("Closing connection")
        self.spi.close_connection()

        

