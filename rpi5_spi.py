import gpiod
import time

MOSI_PIN = 17
SCK_PIN = 11
SS_PIN = 22

CHIP_NAME = "gpiochip4"

chip = gpiod.Chip(CHIP_NAME)

line_mosi = chip.get_line(MOSI_PIN)
line_sck = chip.get_line(SCK_PIN)
line_ss = chip.get_line(SS_PIN)

line_mosi.request(consumer="spi_mosi", type=gpiod.LINE_REQ_DIR_OUT)
line_sck.request(consumer="spi_sck", type=gpiod.LINE_REQ_DIR_OUT)
line_ss.request(consumer="spi_ss", type=gpiod.LINE_REQ_DIR_OUT)

byte_to_send = 0xFF

def send_byte_spi(byte):
    
    line_ss.set_value(0)
    
    for i in range(8):
        line_mosi.set_value((byte >> (7 - i)) & 0x01)
        time.sleep(0.0025)
        line_sck.set_value(1)
        time.sleep(0.0025)
        line_sck.set_value(0)
        time.sleep(0.005)
        
    line_ss.set_value(1)
    
    line_mosi.release()
    line_sck.release()
    line_ss.release()
    
send_byte_spi(byte_to_send)