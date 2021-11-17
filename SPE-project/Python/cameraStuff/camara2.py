import cv2
import numpy as np
import math
import threading
import concurrent.futures
from scipy.cluster.vq import vq, kmeans, whiten
import pandas as pd




class Camara:
    def __init__(self):
        self.num = None
        self.two = None
        self.objects = {}
        self.pixelsX, self.pixelsY = 480, 640
    def get_num(self):
        return self.num

    def get_two(self):
        if self.num == 4:
            return self.two


    def get_objects(self):
        return self.objects

    def get_Feed(self):
        cap = cv2.VideoCapture(1)
        lastcx, lastcy = 0, 0
        numObj = 2

        cm_to_pixel = 39 / 640
        # cm_to_pixel2 = 21 / 323
        while True:
            ret, im = cap.read()
            blue = get_Color(im)
            extra = color_quantization(blue, numObj + 1)
            ret, thresh = cv2.threshold(extra, 127, 255, 0, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            #th3 = cv2.adaptiveThreshold(blue, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 20)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cnts = cv2.drawContours(im, contours, -1, (0, 255, 0), 1)
            pos = []
            posX, posY = [], []
            if len(contours) > 1:
                for j, i in enumerate(contours):
                    m = cv2.moments(i)
                    if m["m00"] != 0:
                        cx = int(m["m10"] / m["m00"])
                        cy = int(m["m01"] / m["m00"])
                        pos.append([cx, cy])
                        posX.append(cx), posY.append(cy)
                        lastcx, lastcy = cx, cy
                        cv2.circle(cnts, (cx, cy), 2, (0, 0, 255), 20)
                        cv2.putText(cnts, f"centroid {j}", (cx - 25, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    if j == 10:
                        break
            if len(pos) == numObj:
                df = pd.DataFrame(list(zip(posX, posY)), columns=['x', 'y'])
                df2 = df.sort_values(by=['x'], ascending=True, ignore_index=True)
                for i in range(numObj):
                    cube = "Cube"+str(i)
                    xs, ys = df2['x'][i],df2['y'][i]
                    self.objects[cube] = [xs, ys]
            cv2.imshow('number_cnts', im)
            cv2.imshow('blue only', blue)
            #cv2.imshow('center_of_mass', extra)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

        cv2.destroyAllWindows()
        cap.release()



def color_quantization(image, k):
    """Performs color quantization using K-means clustering algorithm"""

    # Transform image into 'data':
    # data = np.float32(image).reshape((-1, 1))
    data = np.float32(image)

    # Define the algorithm termination criteria (the maximum number of iterations and/or the desired accuracy):
    # In this case the maximum number of iterations is set to 20 and epsilon = 1.0
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Apply K-means clustering algorithm:
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # At this point we can make the image with k colors
    # Convert center to uint8:
    center = np.uint8(center)
    result = center[label.flatten()]
    return result



def get_Color(im):
    red = im[:, :, 2]
    green = im[:, :, 1]
    blue = im[:, :, 0]

    blue = np.int16(blue) - np.int16(red) - np.int16(green)
    # blue = - np.int16(blue) + np.int16(red) - np.int16(green)

    binary = blue.copy()

    n = 1
    blue[blue < n] = 0
    blue[blue > n] = 255
    binary[binary < n] = 0
    binary[binary > n] = 1
    blue = np.uint8(blue)
    return blue
def getObjectP(l):
    x, y = [i[0] for i in l], [i[1] for i in l]
    return [sum(x)/len(x), sum(y)/len(y)]


"""
camera = Camara()
camera.get_Feed()
"""
