import cv2
import time

class RaspPDI:

    def __init__(self) -> None:
        pass

    def illumination_compesation (self, img):
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

        pdi_img = cv2.merge([channel_b, channel_g, channel_r])

        pdi_img = cv2.cvtColor(pdi_img, cv2.COLOR_BGR2YCrCb)

        Y, Cr, Cb = cv2.split(pdi_img)
        pdi_img = cv2.merge([Cr, Cb, Y])

        mean_time = time.time() - initial_time
        print(f"PDI in rasp finished in: {mean_time}")

        return pdi_img