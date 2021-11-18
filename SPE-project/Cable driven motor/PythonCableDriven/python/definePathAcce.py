import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt
import pandas as pd
import roboticstoolbox as rtb


""" This file is the most extensive !!"""
nexp =4 # exponential constant that affect the acceleration profile
nexp2 =4 # # exponential constant that affect the deceleration profile
nlins =  100 # number of points in the trajectory
here = False
if here:
    nexp = 9
    nexp2 = 9
    nlins = 10


""" Given two points, this function finds the constants in the line equation"""
def lineBetweenTwoPoints(one, two):
    x1, y1 = one[0], one[1]
    x2, y2 = two[0], two[1]
    if abs(x2 - x1) > 0:
        m = (y2 - y1)/( x2 - x1)
    b = y1 - m * x1
    return m, b



def termsExp(n):
    a, b = 0, 0
    b = n/((-1/np.exp(n)) + 1)
    a = -b/np.exp(n)
    return a, b

def termsExpInv(n):
    b = n/(np.exp(-n)- 1)
    a = -b
    return a, b

def expo1(x, init, final):
    n = nexp
    a, b = termsExp(n)
    diff = final[0] - init[0]
    if abs(diff)<0.000001:
        # print(f"diff b4 problems:{diff}")
        diff = final[1] - init[1]
        # print(f"diff problems:{diff}")
        factor = (x - init[1]) * (n / diff)
        f = a + b * np.exp(-factor)
        return init[1] + f * diff * (1 / n)
    factor = (x - init[0]) * (n/diff)
    f = a + b * np.exp(-factor)
    return init[0] + f * diff*(1/n)

def expo2(x, init, final):
    n = nexp2
    a, b = termsExpInv(n)
    diff = final[0] - init[0]
    if abs(diff)<0.000001:
        diff = final[1] - init[1]
        factor = (x - init[1]) * (n / diff)
        f = a + b * np.exp(-factor)
        return init[1] + f * diff * (1 / n)
    factor = (x - init[0]) * (n/diff)
    f = a + b * np.exp(-factor)
    return init[0] + f * diff*(1/n)


""" Returns a trajectory given a initial and a final position"""
def linePath(a, b, expo=False):
    # get the middle point between two points
    middley = (b[1] - a[1]) / 2
    middlex = (b[0] - a[0]) / 2
    diff = abs(b[0] - a[0])

    # check if the points are not in the same x-axis giving and infinity slope
    if diff > 0.01: # if slope not infinity use the equation of the line to ake a path
        t1 = np.linspace(a[0], a[0] + middlex, num=nlins, endpoint=True)
        t2 = np.linspace(a[0] + middlex, b[0], num=nlins, endpoint=True)
        middle = [a[0] + middlex, a[1] + middley]
        l = [expo1(i, a, middle) for i in t1]
        l.reverse()
        l2 = [expo2(i, middle, b) for i in t2]
        l.extend(l2[1:])
        if expo:
            # print(a[0], b[0])
            l = np.linspace(a[0], b[0], num=nlins*2, endpoint=True)
        m, b = lineBetweenTwoPoints(a, b)
        result = [m * i + b for i in l]
        trj = [[i, j] for i, j in zip(l, result)]
        return trj
    else: # if slope infinity just iterate in the y-axis from the initial to final position
        y1 = np.linspace(a[1], a[1] + middley, num=nlins, endpoint=True)
        y2 = np.linspace(a[1] + middley, b[1], num=nlins, endpoint=True)
        middle = [a[0] + middlex, a[1] + middley]
        result = [expo1(i, a, middle) for i in y1]
        result.reverse()
        result2 = [expo2(i, middle, b) for i in y2]
        result.extend(result2[1:])
        l = (a[0]*np.ones(len(result))).tolist()
        trj = [[i,j] for i,j in zip(l, result)]
        return trj


def createPathAcceleartion(xPosObjects, yPosObjects, intiPos, finalPos):
    # Plot the objects position with a radius around them
    angle = np.linspace(0, 2 * np.pi)
    r = 10
    #plt.figure(3)
    #plt.clf()
    for i in range(len(xPosObjects)):
        x = xPosObjects[i] + r * np.cos(angle)
        y = yPosObjects[i] + r * np.sin(angle)
        #plt.plot(x, y, '-', color='red')


    #plt.plot(xPosObjects, yPosObjects, 'ro', color='green')

    xs, ys = [intiPos[0], finalPos[0]], [intiPos[1], finalPos[1]]
    # print("debuging diff :", intiPos[0] - finalPos[0])
    # If the point are located in the same y-position, it means the slope if infinity and cn not be used
    # then just make points N points between the initial and final position
    if abs(intiPos[0] - finalPos[0]) < 1.0:
        trj = []
        for i in range(50):
            trj.append([intiPos[0], (i / 50) * finalPos[1]])
        #print("returning simple: ", trj)
        return trj
    # plot initial and final position
    #plt.plot(xs, ys, '.', color='blue')

    x1 = np.linspace(intiPos[0], finalPos[0], 100)
    m, b1 = lineBetweenTwoPoints(intiPos, finalPos)
    y1 = m * x1 + b1
    plt.plot(x1, y1, '.', color='blue')
    xIntersec, yIntersec = [], []
    for i, j in zip(xPosObjects, yPosObjects):
        for k, l in zip(x1, y1):
            difx = i - k
            dify = j - l
            # if the distance between the point in the line and the radius of the objects is then a threeshold,
            # it means the trajectory collides with radius of the objects
            if abs(difx) < 5 and abs(dify) < 5:
                if i not in xIntersec and j not in yIntersec:
                    # if collides then add the position of objects to a new list
                    xIntersec.append(i)
                    yIntersec.append(j)
                plt.plot(i, j, '.', color='yellow')

    pointsXmin, pointsXmax, pointsYmin, pointsYmax = [], [], [], []
    for i, j in zip(xIntersec, yIntersec):
        x = i + r * np.cos(angle)  # obtain the x-points of the radius
        b2 = j - (-m) * i  # draw a line perpendicular to straight trajectory
        y3, y4 = -m * min(x) + b2, -m * max(x) + b2
        pointsXmin.append(min(x)), pointsYmin.append(y3)
        pointsXmax.append(max(x)), pointsYmax.append(y4)
    plt.plot(pointsXmin, pointsYmin, 'o', color='yellow')
    # it is neccesary to order the colliding points
    # the sort fcntion is not enough fo this  case, so Dataframe makes it easy
    dfmin = pd.DataFrame(list(zip(pointsXmin, pointsYmin)), columns=['x', 'y'])
    dfmax = pd.DataFrame(list(zip(pointsXmax, pointsYmax)), columns=['x', 'y'])
    if finalPos[1] - intiPos[0] <= 0:
        dfmin2 = dfmin.sort_values(by=['x'], ascending=False, ignore_index=True)
        dfmax2 = dfmax.sort_values(by=['x'], ascending=False, ignore_index=True)
    else:
        dfmin2 = dfmin.sort_values(by=['x'], ascending=True, ignore_index=True)
        dfmax2 = dfmax.sort_values(by=['x'], ascending=True, ignore_index=True)
    trjs = []
    rare = True
    if len(pointsYmin) > 1:
        print("dfmin2: ", dfmin2)
        for i in range(len(pointsYmin) - 1):
            if i == 0:
                a, b = intiPos, [dfmin2['x'][i], dfmin2['y'][i]]
                trj = linePath(a, b, expo=False)
                trjs.append(trj)
                rare = False
                """
                if len(pointsYmin) - 2 == 0:
                    print("I am here strange")
                    a, b = [dfmin2['x'][i + 1], dfmin2['y'][i + 1]], finalPos
                    trj = linePath(a, b, expo=False)
                    trjs.append(trj)
                """
            a, b = [dfmin2['x'][i], dfmin2['y'][i]], [dfmin2['x'][i + 1], dfmin2['y'][i + 1]]
            trj = linePath(a, b, expo=False)
            trjs.append(trj)
            if i == len(pointsYmin) - 2:
                a, b = [dfmin2['x'][i + 1], dfmin2['y'][i + 1]], finalPos
                trj = linePath(a, b, expo=False)
                trjs.append(trj)
    elif len(pointsYmin) == 1:
        i = 0
        a, b = intiPos, [dfmin2['x'][i], dfmin2['y'][i]]
        trj = linePath(a, b, expo=False)
        trjs.append(trj)
        a, b = [dfmin2['x'][i], dfmin2['y'][i]], finalPos
        trj = linePath(a, b, expo=False)
        trjs.append(trj)
    elif len(pointsYmin) == 0:
        a, b = intiPos, finalPos
        trj = linePath(a, b, expo=False)
        trjs.append(trj)
    trj, trjx, trjy = [], [], []


    counter = 0
    for i in trjs:
        counter += 1
        for j in i:
            # print(j)
            trj.append([j[0], j[1]])
            trjx.append(j[0])
            trjy.append(j[1])


    # plt.plot(trjx, trjy, 'o', color='green')
    #plt.pause(2)
    # plt.show()
    return trj



def drawEndEffector(x, y):
    square = 5.1
    xp, yp = [], []
    xp.append(x-square/2), xp.append(x + square/2), xp.append(x+square/2), xp.append(x - square/2), xp.append(x-square/2)
    yp.append(y - square / 2), yp.append(y - square / 2), yp.append(y + square / 2), yp.append(y + square / 2), yp.append(y - square / 2)

    plt.plot(xp, yp, '-', c='black')

def getInitialLenghts(lenght):
    l = lenght
    side = 5.1  # dimension of the one side of the end effector, taken as square (it must be in cm)
    side = side / 2
    xs, ys = [side, -side, -side, side], [side, side, -side, -side]
    ld, lu, ls, lo = 95.98 / 2.0, 95.98 / 2.0, 99.84 / 2.0, 99.84 / 2.0
    xl, yl = [lu, -lu, -ld, ld], [ls, lo, -lo, -ls]
    lengths = []
    counter = 0
    for i, j, k, m in zip(xl, yl, xs ,ys):
        lengths.append(np.sqrt((i - k)**2 + (j - m)**2))
    return lengths[0], lengths[1], lengths[2], lengths[3]


"""Given a position in x and y, it finds the lengths of each string"""
def calculateLenghts(x, y, l):
    side = 5.1  # dimension of the one side of the end effector, taken as square (it must be in cm)
    side = side / 2
    xs, ys = [side, -side, -side, side], [side, side, -side, -side]
    # xl, yl = [l, -l, -l, l], [l, l, -l, -l]
    ld, lu, ls, lo = 95.98 / 2.0, 95.98 / 2.0, 99.84 / 2.0, 99.84 / 2.0
    xl, yl = [lu, -lu, -ld, ld], [ls, lo, -lo, -ls]
    lengths = []
    for i, j, k, m in zip(xl, yl, xs, ys):
        lengths.append(np.sqrt((i - (k + x)) ** 2 + (j - (m + y)) ** 2))
    return lengths[0], lengths[1], lengths[2], lengths[3]


""" For plotting the lengths of the robot"""
def drawLinks(l, x, y):
    side = 5.1 # dimension of the one side of the end effector, taken as square (it must be in cm)
    side = side/2
    xs, ys = [side, -side, -side, side], [side, side, -side, -side]
    # xl, yl = [l, -l, -l, l],[l, l, -l,-l]
    ld, lu, ls, lo = 95.98/2.0, 95.98/2.0, 99.84/2.0 , 99.84/2.0
    xl, yl = [lu, -lu, -ld, ld], [ls, lo, -lo, -ls]
    plt.plot(xl, yl, 'o', c='blue')
    # lines
    for i, j, k, m in zip(xl, yl, xs ,ys):
        plt.plot([x + k, i], [y + m, j],'-', c='black')


def getTrajectoryLengths(length, a, b, trj):
    il1, il2, il3, il4 = getInitialLenghts(length)
    ls = []
    counter = 0
    for i in trj:
        fl1, fl2, fl3, fl4 = calculateLenghts(i[0], i[1], length)
        fl1, fl2, fl3, fl4 = fl1 - il1, fl2 - il2, fl3 - il3, fl4 - il4
        ls.append([fl1, fl2, fl3, fl4])

    return ls


"""Plots the animation of the end effector moving over the table"""
def plotTrajectoryCable(length, a, b, trj):
    plt.figure(4)
    plt.ion()
    for i in trj:
        plt.clf()
        plt.plot([a[0], b[0]], [a[1], b[1]], 'o', color='red')
        drawLinks(length, i[0], i[1])
        drawEndEffector(i[0], i[1])
        plt.axis(xmin=-length, xmax=length, ymin=-length, ymax=length)
        plt.pause(0.01)
        plt.show()




""" This section is only for debugging  """
if here:
    a = [-10, -30]
    b = [10.0, -30]

    trj1= linePath(a, b, expo=False)

    qt = getTrajectoryLengths(45, a, b, trj1)
    reach = 50
    plotTrajectoryCable(reach, a, b, trj1)
    print(trj1)


    """
    xObjects = [-5,  5, -20, -10]
    yObjects = [-15, 15, 20, 10]
    trj = createPathAcceleartion(xObjects, yObjects,a, b )
    length = 45
    plt.figure(1)
    plt.clf()
    plt.axis(xmin=-length, xmax=length, ymin=-length, ymax=length)
    drawEndEffector(a[0], a[1])
    drawEndEffector(b[0], b[1])
    plt.show()
    plt.figure(4)
    plt.ion()
    for i in trj:

        plt.clf()
        plt.plot([a[0], b[0]], [a[1], b[1]], 'o', color='red')
        drawLinks(length, i[0], i[1])
        plt.axis(xmin=-length, xmax=length, ymin=-length, ymax=length)
        plt.pause(0.01)
        plt.show()
    """