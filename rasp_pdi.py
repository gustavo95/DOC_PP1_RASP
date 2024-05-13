import cv2
import time
import numpy as np

class RaspPDI:

    def __init__(self) -> None:
        pass

    def illumination_compesation (self, img):
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

        return pdi_img
    
    def skin_color_segmentation(self, Y, Cr, Cb):
        cb_min, cb_max = 95, 120
        cr_min, cr_max = 140, 170

        mask_cb = cv2.inRange(Cb, cb_min, cb_max)
        mask_cr = cv2.inRange(Cr, cr_min, cr_max)

        mask = cv2.bitwise_and(mask_cb, mask_cr)

        return mask
    
    def filtering(self, img):
        kernel = np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ], dtype=np.uint8)

        eroded_img = cv2.erode(img, kernel, iterations=1)
        dilated_img = cv2.dilate(eroded_img, kernel, iterations=1)

        return dilated_img
    
    