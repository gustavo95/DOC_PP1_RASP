import cv2
import time
from rasp_pdi import RaspPDI
from communication_controller import CommunicationController

def rasp_pdi(img):
    initial_time = time.time()
    pdi = RaspPDI()

    img = pdi.illumination_compesation(img)
    
    img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(img_YCrCb)
    # img = cv2.merge([Cr, Cb, Y])
    
    img = pdi.skin_color_segmentation(Y, Cr, Cb)
    img = pdi.filtering(img)
    
    area, perimeter = pdi.hand_area_perimeter(img)
    print(f"RPi - Area: {area}, Perimeter: {perimeter}")

    mean_time = time.time() - initial_time
    print(f"PDI in rasp finished in: {mean_time}")
    # cv2.imshow("rpi_img", img)

def fpga_pdi(img, height, width):
    initial_time = time.time()
    com = CommunicationController(height, width)

    com.send_rgb_img(img)

    print("Image send")
    # time.sleep(2)

    com.run_pdi()
    # time.sleep(2)

    # new_img_r = com.recive_img(0b01)
    # new_img_g = com.recive_img(0b10)
    # new_img_b = com.recive_img(0b11)
    # new_img = cv2.merge([new_img_b, new_img_g, new_img_r])
    
    hand_area = com.recive_int_32bits(0b00)
    hand_perimeter = com.recive_int_32bits(0b01)
    print(f"FPGA - Area: {hand_area}, Perimeter: {hand_perimeter}")

    com.close_communication()

    fpga_time = time.time() - initial_time
    print(f"FPGA finished in: {fpga_time}")
    # cv2.imshow("fpga_img", new_img)

def main():
    height = 240
    width = 320
    
    # img = cv2.imread('hand.jpg')
    # img = cv2.imread('one_finger_up.JPEG')
    # img = cv2.imread('victory.JPEG')
    # img = cv2.imread('three_fingers_up.JPEG')
    # img = cv2.imread('four_fingers_up.JPEG')
    img = cv2.imread('open_palm.JPEG')
    # img = cv2.imread('closed_fist.JPEG')
    
    img = cv2.resize(img, (width, height))

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    fpga_pdi(img, height, width)

    rasp_pdi(img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()