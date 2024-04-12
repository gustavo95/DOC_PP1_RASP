import cv2
import time
from communication_controller import CommunicationController

def pdi(img):
    initial_time = time.time()
    height, width = img.shape[0:2]
    channel_b, channel_g, channel_r = cv2.split(img)

    mean_r = cv2.mean(channel_r)[0]
    print("R mean:", mean_r)
    mean_g = cv2.mean(channel_g)[0]
    print("G mean:", mean_g)
    mean_b = cv2.mean(channel_b)[0]
    print("B mean:", mean_b)

    max_mean = mean_r
    if (mean_g > max_mean):
        max_mean = mean_g
    if (mean_b > max_mean):
        max_mean = mean_b

    red_gain = mean_r/max_mean
    green_gain = mean_g/max_mean
    blue_gain = mean_b/max_mean

    for i in range(height):
        for j in range(width):
            channel_r[i,j] = channel_r[i,j]*red_gain
            channel_g[i,j] = channel_g[i,j]*green_gain
            channel_b[i,j] = channel_b[i,j]*blue_gain

    mean_time = time.time() - initial_time
    print(f"PDI in rasp finished in: {mean_time}")

    pdi_img = cv2.merge([channel_b, channel_g, channel_r])
    return pdi_img


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

    com.run_pdi()
    time.sleep(2)

    new_img_r = com.recive_img(0b01)
    # cv2.imshow("new_img_r", new_img_r)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    new_img_g = com.recive_img(0b10)
    # cv2.imshow("new_img_g", new_img_g)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    new_img_b = com.recive_img(0b11)
    # cv2.imshow("new_img_b", new_img_b)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    new_img = cv2.merge([new_img_b, new_img_g, new_img_r])
    cv2.imshow("fpga_img", new_img)

    pdi_img = pdi(img)
    cv2.imshow("rpi_img", pdi_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    com.close_communication()

if __name__ == "__main__":
    main()