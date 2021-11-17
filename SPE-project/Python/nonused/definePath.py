import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import roboticstoolbox as rtb


def lineBetweenTwoPoints(one, two):
    x1, y1 = one[0], one[1]
    x2, y2 = two[0], two[1]
    if abs(x2 - x1) > 0:
        m = (y2 - y1)/( x2 - x1)
        # print("normal m: ", m)
    else:
        m = (y2 - y1)/( x2 - x1)
        # print("unexpected m: ", m)
    b = y1 - m*x1
    #print(b)
    return m, b


def createPath(xPosObjects, yPosObjects, intiPos, finalPos):
    plt.figure(4)
    plt.cla()
    angle = np.linspace(0, 2 * np.pi)
    r = 0.2
    for i in range(len(xPosObjects)):
        x = xPosObjects[i] + r * np.cos(angle)
        y = yPosObjects[i] + r * np.sin(angle)
        plt.plot(x, y, '-', color='red')
    plt.plot(xPosObjects, yPosObjects, 'ro', color='green')
    xs, ys = [intiPos[0], finalPos[0]],[intiPos[1], finalPos[1]]
    plt.plot(xs, ys, '.', color='blue')
    x1 = np.linspace(intiPos[0], finalPos[0], 50)
    m, b1 =lineBetweenTwoPoints(intiPos, finalPos)
    y1 = m * x1 + b1
    plt.plot(x1, y1, '.', color='blue')
    xIntersec, yIntersec = [], []
    for i, j in zip(xPosObjects, yPosObjects):
        for k, l in zip(x1, y1):
            difx = i - k
            dify = j - l
            if abs(difx)< 0.2 and abs(dify) < 0.2:
                if i not in xIntersec and j not in yIntersec:
                    xIntersec.append(i)
                    yIntersec.append(j)
                plt.plot(i, j, '.', color='yellow')
    pointsXmin, pointsXmax, pointsYmin, pointsYmax = [], [], [], []
    for i, j in zip(xIntersec, yIntersec):
        x = i + r * np.cos(angle)
        b2 = j - (-m) * i
        y3, y4 = -m * min(x) + b2, -m * max(x) + b2
        pointsXmin.append(min(x)), pointsYmin.append(y3)
        pointsXmax.append(max(x)), pointsYmax.append(y4)
    plt.plot(pointsXmin, pointsYmin, 'o', color='red')
    # plt.plot(pointsXmax, pointsYmax, 'o', color='red')
    dfmin = pd.DataFrame(list(zip(pointsXmin, pointsYmin)), columns=['x', 'y'])
    dfmax = pd.DataFrame(list(zip(pointsXmax, pointsYmax)), columns=['x', 'y'])
    if finalPos[1] - intiPos[0] >= 0:
        dfmin2 = dfmin.sort_values(by=['x'], ascending=False, ignore_index=True)
        dfmax2 = dfmax.sort_values(by=['x'], ascending=False, ignore_index=True)
    else:
        dfmin2 = dfmin.sort_values(by=['x'], ascending=True, ignore_index=True)
        dfmax2 = dfmax.sort_values(by=['x'], ascending=True, ignore_index=True)
    trjx, trjy = [], []
    rare = True
    if len(pointsYmin)  > 1:
        for i in range(len(pointsYmin) - 1):
            print("I am here")
            if i == 0:
                m5, b5 = lineBetweenTwoPoints(intiPos, [dfmin2['x'][i], dfmin2['y'][i]])
                x5 = np.linspace(intiPos[0],dfmin2['x'][i], 100)
                y5 = m5 * x5 + b5
                plt.plot(x5, y5, '-', color='black')
                trjx.append(x5), trjy.append(y5)
                rare = False
                if len(pointsYmin) - 2 == 0:
                    m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i+1], dfmin2['y'][i+1]], finalPos)
                    x5 = np.linspace(dfmin2['x'][i+1], finalPos[0], 50)
                    y5 = m5 * x5 + b5
                    plt.plot(x5, y5, '--', color='black')
                    trjx.append(x5), trjy.append(y5)
            m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i], dfmin2['y'][i]], [dfmin2['x'][i + 1], dfmin2['y'][i + 1]])
            x5 = np.linspace(dfmin2['x'][i], dfmin2['x'][i + 1], 50)
            y5 = m5 * x5 + b5
            plt.plot(x5, y5, '-', color='black')
            trjx.append(x5), trjy.append(y5)
            if i == len(pointsYmin) - 2 or (i == 0 and rare == True):
                m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i+1], dfmin2['y'][i+1]], finalPos)
                x5 = np.linspace(dfmin2['x'][i+1], finalPos[0], 50)
                y5 = m5 * x5 + b5
                plt.plot(x5, y5, '-', color='black')
                trjx.append(x5), trjy.append(y5)
    elif len(pointsYmin) == 1:
        i = 0
        m5, b5 = lineBetweenTwoPoints(intiPos, [dfmin2['x'][i], dfmin2['y'][i]])
        x5 = np.linspace(intiPos[0], dfmin2['x'][i], 50)
        y5 = m5 * x5 + b5
        plt.plot(x5, y5, '-', color='black')
        trjx.append(x5), trjy.append(y5)
        m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i ], dfmin2['y'][i]], finalPos)
        x5 = np.linspace(dfmin2['x'][i], finalPos[0], 50)
        y5 = m5 * x5 + b5
        plt.plot(x5, y5, '-', color='black')
        trjx.append(x5), trjy.append(y5)
    elif len(pointsYmin)==0:
        m5, b5 = lineBetweenTwoPoints(intiPos, finalPos)
        x5 = np.linspace(intiPos[0], finalPos[0], 50)
        y5 = m5 * x5 + b5
        plt.plot(x5, y5, '-', color='black')
        trjx.append(x5), trjy.append(y5)

    trj = []
    for i, j in zip(trjx, trjy):
        for k, l in zip(i, j):
            trj.append([k,l])
    #plt.show()
    return trj

def inverseGenerator(trj, initThetax, initThetay):
    thetas = []
    l1,l2 = 2, 2
    counter = 0
    theta1, theta2 = initThetax, initThetay
    for i in trj:
        x, y = i[0], i[1]
        if np.sqrt(x ** 2 + y ** 2) > l1 + l2:
            # print("shouldnt :", np.sqrt(x ** 2 + y ** 2), " > ", l1+l2)
            theta2_goal = 0
        else:
            theta2_goal = np.arccos(
                (x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))

        # print("theta goal 2: ", theta2_goal, " distance: ", np.sqrt(x ** 2 + y ** 2), 'li nd l2: ', l1 +l2 )
        tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                            (l1 + l2 * np.cos(theta2_goal)))
        theta1_goal = np.math.atan2(y, x) - tmp
        if counter == 10:
            theta1, theta2 = initThetax, initThetay
            # thetas.append([theta1_goal, theta2_goal])
            counter = counter + 1
            continue
        if not math.isnan(theta1_goal) and  not math.isnan(theta1_goal):
            # print(theta1_goal, " : ", theta2_goal)
            pi = np.pi
            thetas.append([theta1 - ang_diff(theta1, theta1_goal), theta2 - ang_diff(theta2, theta2_goal)])
            # print(theta1*(360/(2*pi)), ang_diff(theta1, theta1_goal)*(360/(2*pi)), (theta1 - ang_diff(theta1, theta1_goal))*(360/(2*pi)), theta1_goal*(360/(2*pi)))
            # theta1 = theta1_goal
            # theta2 = theta2_goal
            theta1 = theta1 - ang_diff(theta1, theta1_goal)
            theta2 = theta2 - ang_diff(theta2, theta2_goal)
            #thetas.append([theta1_goal, theta2_goal])


    return np.array(thetas)


def createPath2(xPosObjects, yPosObjects, intiPos, finalPos):
    #plt.figure(4)
    #plt.cla()
    angle = np.linspace(0, 2 * np.pi)
    r = 0.2
    for i in range(len(xPosObjects)):
        x = xPosObjects[i] + r * np.cos(angle)
        y = yPosObjects[i] + r * np.sin(angle)
        plt.plot(x, y, '-', color='red')
    plt.plot(xPosObjects, yPosObjects, 'ro', color='green')
    xs, ys = [intiPos[0], finalPos[0]],[intiPos[1], finalPos[1]]
    print("debuging diff :",intiPos[0]-finalPos[0])
    if abs(intiPos[0]-finalPos[0]) < 1.0:
        trj = []
        for i in range(50):
            trj.append([intiPos[0], (i/50)*finalPos[1]])
        print("returning simple: ", trj)
        return trj
    plt.plot(xs, ys, '.', color='blue')
    x1 = np.linspace(intiPos[0], finalPos[0], 50)
    m, b1 =lineBetweenTwoPoints(intiPos, finalPos)
    y1 = m * x1 + b1
    plt.plot(x1, y1, '.', color='blue')
    xIntersec, yIntersec = [], []
    for i, j in zip(xPosObjects, yPosObjects):
        for k, l in zip(x1, y1):
            difx = i - k
            dify = j - l
            if abs(difx)< 0.2 and abs(dify) < 0.2:
                if i not in xIntersec and j not in yIntersec:
                    xIntersec.append(i)
                    yIntersec.append(j)
                plt.plot(i, j, '.', color='yellow')
    pointsXmin, pointsXmax, pointsYmin, pointsYmax = [], [], [], []
    for i, j in zip(xIntersec, yIntersec):
        x = i + r * np.cos(angle)
        b2 = j - (-m) * i
        y3, y4 = -m * min(x) + b2, -m * max(x) + b2
        pointsXmin.append(min(x)), pointsYmin.append(y3)
        pointsXmax.append(max(x)), pointsYmax.append(y4)
    plt.plot(pointsXmin, pointsYmin, 'o', color='red')
    # plt.plot(pointsXmax, pointsYmax, 'o', color='red')
    dfmin = pd.DataFrame(list(zip(pointsXmin, pointsYmin)), columns=['x', 'y'])
    dfmax = pd.DataFrame(list(zip(pointsXmax, pointsYmax)), columns=['x', 'y'])
    dfmin2 = dfmin.sort_values(by=['x'], ascending=False, ignore_index=True)
    dfmax2 = dfmax.sort_values(by=['x'], ascending=False, ignore_index=True)
    trjx, trjy = [], []
    rare = True
    if len(pointsYmin)  > 1:
        for i in range(len(pointsYmin) - 1):
            print("I am here")
            if i == 0:
                m5, b5 = lineBetweenTwoPoints(intiPos, [dfmin2['x'][i], dfmin2['y'][i]])
                x5 = np.linspace(intiPos[0],dfmin2['x'][i], 100)
                y5 = m5 * x5 + b5
                plt.plot(x5, y5, '-', color='black')
                trjx.append(x5), trjy.append(y5)
                rare = False
                if len(pointsYmin) - 2 == 0:
                    m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i+1], dfmin2['y'][i+1]], finalPos)
                    x5 = np.linspace(dfmin2['x'][i+1], finalPos[0], 50)
                    y5 = m5 * x5 + b5
                    plt.plot(x5, y5, '--', color='black')
                    trjx.append(x5), trjy.append(y5)
            m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i], dfmin2['y'][i]], [dfmin2['x'][i + 1], dfmin2['y'][i + 1]])
            x5 = np.linspace(dfmin2['x'][i], dfmin2['x'][i + 1], 50)
            y5 = m5 * x5 + b5
            plt.plot(x5, y5, '-', color='black')
            trjx.append(x5), trjy.append(y5)
            if i == len(pointsYmin) - 2 or (i == 0 and rare == True):
                m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i+1], dfmin2['y'][i+1]], finalPos)
                x5 = np.linspace(dfmin2['x'][i+1], finalPos[0], 50)
                y5 = m5 * x5 + b5
                plt.plot(x5, y5, '-', color='black')
                trjx.append(x5), trjy.append(y5)
    elif len(pointsYmin) == 1:
        i = 0
        m5, b5 = lineBetweenTwoPoints(intiPos, [dfmin2['x'][i], dfmin2['y'][i]])
        x5 = np.linspace(intiPos[0], dfmin2['x'][i], 50)
        y5 = m5 * x5 + b5
        plt.plot(x5, y5, '-', color='black')
        trjx.append(x5), trjy.append(y5)
        m5, b5 = lineBetweenTwoPoints([dfmin2['x'][i ], dfmin2['y'][i]], finalPos)
        x5 = np.linspace(dfmin2['x'][i], finalPos[0], 50)
        y5 = m5 * x5 + b5
        plt.plot(x5, y5, '-', color='black')
        trjx.append(x5), trjy.append(y5)
    elif len(pointsYmin)==0:
        m5, b5 = lineBetweenTwoPoints(intiPos, finalPos)
        x5 = np.linspace(intiPos[0], finalPos[0], 50)
        y5 = m5 * x5 + b5
        plt.plot(x5, y5, '-', color='black')
        trjx.append(x5), trjy.append(y5)

    trj = []
    for i, j in zip(trjx, trjy):
        for k, l in zip(i, j):
            trj.append([k,l])
    #plt.show()
    return trj

def ang_diff(theta1, theta2):
    # Returns the difference between two angles in the range -pi to +pi
    return (theta1 - theta2 + np.pi) % (2 * np.pi) - np.pi



a = [1.5, 3.8]
b = [-1.5, -3.5]
xObjects = [0.4, 0.25, -0.183, -1.3, 1.7]
yObjects = [1.18, -1.9, -0.3, 0.5, 0.59]

robot = rtb.models.DH.Planar2()
robot.links[0].a = 2
robot.links[1].a = 2
trj = createPath2(xObjects, yObjects, a, b)
angles = inverseGenerator(trj, 0.0, 0.0)
print(trj)
#robot.plot(angles, block=False, jointaxes=True, shadow=True)
plt.show()



