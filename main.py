import cv2
import time
from communication_controller import CommunicationController

def main():
    com = CommunicationController()

    img = cv2.imread('hand.jpg')
    img = cv2.resize(img, (160, 120))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    com.send_img(img)

    print("Image send")
    time.sleep(1)

    new_img = com.recive_img()

    cv2.imshow("new_img", new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    com.close_communication()

if __name__ == "__main__":
    main()