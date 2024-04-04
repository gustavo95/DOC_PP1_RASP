import cv2
from communication_controller import CommunicationController

def main():
    com = CommunicationController()

    img = cv2.imread('hand.jpg')
    img = cv2.resize(img, (320, 240))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow("img", img)
    cv2.waitKey(0)

    com.send_img(img)
    com.close_communication()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()