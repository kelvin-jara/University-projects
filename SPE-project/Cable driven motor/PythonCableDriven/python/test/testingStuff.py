import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt
import pandas as pd
import roboticstoolbox as rtb

nexp =4
nexp2 =4
nlins =  300
here = True
if here:
    nexp = 9
    nexp2 = 9
    nlins = 25
def drawEndEffector(x, y):
    square = 10
    xp, yp = [], []
    xp.append(x-square/2), xp.append(x + square/2), xp.append(x+square/2), xp.append(x - square/2), xp.append(x-square/2)
    yp.append(y - square / 2), yp.append(y - square / 2), yp.append(y + square / 2), yp.append(y + square / 2), yp.append(y - square / 2)

    plt.plot(xp, yp, '-', c='black')

def calculateLenghts(x, y):
    angle = np.arctan2(y, x)
    l1, l2 = L*np.cos(angle), L*np.sin(ange)
    return l1, l2

def drawLinks(l, x, y):
    xl, yl = [l, -l, -l, l],[l, l, -l,-l]
    plt.plot(xl, yl, 'o', c='blue')
    # lines
    for i, j in zip(xl, yl):
        plt.plot([x, i], [y, j],'-', c='black')
    l1, l2 = calculateLenghts(x, y)
    print(l1, l2)

if here:
    a = [-10, -30]
    b = [10.0, 30]
    length = 45

    drawEndEffector(a[0], a[1])
    drawEndEffector(b[0],b[1])
    drawLinks(length, a[0], a[1])
    plt.plot([a[0], b[0]], [a[1], b[1]], 'o', color='red')
    plt.axis(xmin=-length, xmax=length, ymin=-length, ymax=length)
    plt.show()