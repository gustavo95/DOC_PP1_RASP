import cv2
import time
from communication_controller import CommunicationController

def main():
    height = 240
    width = 320
    com = CommunicationController(height, width)
    
    img = cv2.imread('hand.jpg')
    img = cv2.resize(img, (width, height))

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    com.send_rgb_img(img)

    print("Image send")
    time.sleep(2)

    new_img_r = com.recive_img(0b01)
    cv2.imshow("new_img_r", new_img_r)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    new_img_g = com.recive_img(0b10)
    cv2.imshow("new_img_g", new_img_g)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    new_img_b = com.recive_img(0b11)
    cv2.imshow("new_img_b", new_img_b)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    new_img = cv2.merge([new_img_b, new_img_g, new_img_r])
    cv2.imshow("new_img", new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    com.close_communication()

if __name__ == "__main__":
    main()