import cv2
import numpy as np
import math
import threading
import concurrent.futures


class Camara:
    def __init__(self):
        self.num = None
        self.two = None

    def get_num(self):
        return self.num

    def get_two(self):
        if self.num == 4:
            return self.two

    def get_Feed(self):
        cap = cv2.VideoCapture(1)
        cm_to_pixel = 39 / 640
        #cm_to_pixel2 = 21 / 323
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            red = frame[:, :, 2]
            green = frame[:, :, 1]
            blue = frame[:, :, 0]
            """
            red_only = np.int16(red) - np.int16(green) - np.int16(blue)
            red_only[red_only < 0] = 0
            red_only[red_only > 255] = 255
            red_only = np.uint8(red_only)
            
            white = np.int16(red) + np.int16(green) + np.int16(blue)
            white[white < 760] = 0
            white[white > 760] = 255
            white = np.uint8(white)
            """
            blue = np.int16(blue) - np.int16(red) - np.int16(green)
            n = 200
            blue[blue < n] = 0
            blue[blue > n] = 255
            blue = np.uint8(blue)
            print(blue.shape)
            red_only = blue
            column_sums = np.matrix(np.sum(red_only, 0))
            column_numbers = np.matrix(np.arange(640))
            column_mult = np.multiply(column_sums, column_numbers)
            total = np.sum(column_mult)
            total_total = np.sum(np.sum(red_only))
            column_location = total / total_total

            X_location = column_location * cm_to_pixel

            row_sums = np.matrix(np.sum(red_only, 1))
            row_sums = row_sums.transpose()
            row_numbers = np.matrix(np.arange(480))
            row_mult = np.multiply(row_sums, row_numbers)
            total2 = np.sum(row_mult)
            total_total2 = np.sum(np.sum(red_only))
            row_location = total2 / total_total2
            Y_location = 0
            print(f"location X:{X_location} and Y:{Y_location}")
            # print(white)
            cv2.imshow('red_only', blue)
            # cv2.imshow('frame', frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

        cv2.destroyAllWindows()
        cap.release()


camera = Camara()
camera.get_Feed()