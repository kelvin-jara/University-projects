import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt
import pandas as pd
import roboticstoolbox as rtb

nexp =4
nexp2 =4

""" Number of point in the trajectory"""
nlins =  75

def lineBetweenTwoPoints(one, two):
    x1, y1 = one[0], one[1]
    x2, y2 = two[0], two[1]
    if abs(x2 - x1) > 0:
        m = (y2 - y1)/( x2 - x1)
    b = y1 - m * x1
    return m, b

def createPath3(xPosObjects, yPosObjects, intiPos, finalPos):
    plt.plot([intiPos[0], finalPos[0]], [intiPos[1], finalPos[1]], 'o', color='red')

    x1 = np.linspace(intiPos[0], finalPos[0], 50)
    m, b1 = lineBetweenTwoPoints(intiPos, finalPos)
    y1 = m * x1 + b1
    plt.plot(x1, y1, '.', color='blue')

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

def linePath(a, b, expo=False):

    middley = (b[1] - a[1]) / 2
    middlex = (b[0] - a[0]) / 2
    diff = abs(b[0] - a[0])
    if diff > 0.01:
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
    else:
        y1 = np.linspace(a[1], a[1] + middley, num=nlins, endpoint=True)
        y2 = np.linspace(a[1] + middley, b[1], num=nlins, endpoint=True)
        middle = [a[1] + middlex, a[1] + middley]
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
    #plt.plot(pointsXmin, pointsYmin, 'o', color='yellow')
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
        print("I am here")
        for i in range(len(pointsYmin) - 1):
            if i == 0:

                a, b = intiPos, [dfmin2['x'][i], dfmin2['y'][i]]
                trj = linePath(a, b, expo=False)
                trjs.append(trj)
                rare = False
                if len(pointsYmin) - 2 == 0:

                    a, b = [dfmin2['x'][i + 1], dfmin2['y'][i + 1]], finalPos
                    trj = linePath(a, b, expo=False)
                    trjs.append(trj)

            a, b = [dfmin2['x'][i], dfmin2['y'][i]], [dfmin2['x'][i + 1], dfmin2['y'][i + 1]]
            trj = linePath(a, b, expo=False)
            trjs.append(trj)
            if i == len(pointsYmin) - 2 or (i == 0 and rare == False):

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


    #plt.plot(trjx, trjy, 'o', color='green')
    #plt.pause(2)
    #plt.show()
    return trj


def inverseGenerator(trj, initThetax, initThetay):
    thetas = []
    l1,l2 = 24, 21.5
    theta1, theta2 = initThetax, initThetay
    changed = False
    counter  = 0
    for i in trj:
        x, y = i[0], i[1]
        if np.sqrt(x ** 2 + y ** 2) > l1 + l2:
            theta2_goal = 0
        else:
            theta2_goal = np.arccos((x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2))

        tmp = np.math.atan2(l2 * np.sin(theta2_goal), (l1 + l2 * np.cos(theta2_goal)))
        theta1_goal = np.math.atan2(y, x) - tmp
        see = True
        if theta2_goal < 0:
        # if see:
            """
            theta2_goal = -theta2_goal
            tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                               (l1 + l2 * np.cos(theta2_goal)))"""
            theta1_goal = np.math.atan2(y, x) + tmp
        if not math.isnan(theta1_goal) and  not math.isnan(theta1_goal):
            # print(theta1_goal, " : ", theta2_goal)

            pi = np.pi
            if counter == 0:
                #thetas.append([initThetay, initThetay])
                counter += 1
            angle  = [theta1 - ang_diff(theta1, theta1_goal), theta2 - ang_diff(theta2, theta2_goal)]
            # angle = [theta1_goal, theta2_goal]
            thetas.append(angle)
            # print(theta1*(360/(2*pi)), ang_diff(theta1, theta1_goal)*(360/(2*pi)), (theta1 - ang_diff(theta1, theta1_goal))*(360/(2*pi)), theta1_goal*(360/(2*pi)))
            # theta1 = theta1_goal
            # theta2 = theta2_goal
            theta1 = angle[0]
            theta2 = angle[1]
    return np.array(thetas)

def ang_diff(theta1, theta2):
    # Returns the difference between two angles in the range -pi to +pi
    return (theta1 - theta2 + np.pi) % (2 * np.pi) - np.pi

def plotTrj(qt, l1, l2, endeffector=False, real=None):
    plt.figure(1)
    #plt.cla()
    if not endeffector:  # used to make an animation of what the robotic manipulator will do
        plt.ion()
        for i in qt:
            plt.cla()
            x1, y1 = [0, l1 * np.cos(i[0])], [0, l1 * np.sin(i[0])]
            x2, y2 = [l1 * np.cos(i[0]), l1 * np.cos(i[0]) + l2 * np.cos(i[1]+i[0])], [l1 * np.sin(i[0]),l1 * np.sin(i[0]) + l2 * np.sin(i[1]+i[0])]

            plt.plot(x1, y1, '-', color='black')
            plt.plot(x2, y2, '-', color='blue')
            plt.axis(xmin=-l1-l2, xmax=l1+l2, ymin=-l1-l2, ymax=l1+l2)
            # plt.show()
            plt.pause(0.0001)
        plt.ioff()
    else:
        plt.cla()
        plt.ion()
        real = real*360.0/(2.0*np.pi)
        x, y = [i[0] for i in qt], [i[1] for i in qt]
        xr, yr = [i[0] for i in real], [i[1] for i in real]
        xp, yp = [], []
        xrp, yrp = [], []
        for i in real:
            i = i*(2*np.pi)/360.0
            xrp.append(l1 * np.cos(i[0]) + l2 * np.cos(i[1] + i[0]))
            yrp.append( l1 * np.sin(i[0]) + l2 * np.sin(i[1] + i[0]))
        for i in qt:
            i = i * ((2 * np.pi) / 360.0)
            xp.append(l1 * np.cos(i[0]) + l2 * np.cos(i[1] + i[0]))
            yp.append(l1 * np.sin(i[0]) + l2 * np.sin(i[1] + i[0]))
        #plt.plot(x, y, '.', color='blue')
        #plt.plot(xr, yr, '.', color='red')
        plt.plot(xp, yp, '.', color='red', label='Followed trajectory')
        plt.plot(xrp, yrp, '.', color='green', label='Expected trajectory')
        i = real[0]
        i = i * ((2 * np.pi) / 360.0)
        x1i, y1i = [0, l1 * np.cos(i[0])], [0, l1 * np.sin(i[0])]
        x2i, y2i = [l1 * np.cos(i[0]), l1 * np.cos(i[0]) + l2 * np.cos(i[1] + i[0])], [l1 * np.sin(i[0]),l1 * np.sin(i[0]) + l2 * np.sin(i[1] + i[0])]
        i = real[-1]
        i = i * ((2 * np.pi) / 360.0)
        x1f, y1f = [0, l1 * np.cos(i[0])], [0, l1 * np.sin(i[0])]
        x2f, y2f = [l1 * np.cos(i[0]), l1 * np.cos(i[0]) + l2 * np.cos(i[1] + i[0])], [l1 * np.sin(i[0]), l1 * np.sin(i[0]) + l2 * np.sin(i[1] + i[0])]
        t = 7
        plt.plot(x1i, y1i, '-', color='black',linewidth=t, label="Initial Position")
        plt.plot(x2i, y2i, '-', color='black',linewidth=t)
        plt.plot(x1f, y1f, '-', color='blue',linewidth=t, label="Final Position")
        plt.plot(x2f, y2f, '-', color='blue',linewidth=t)
        plt.legend()
        plt.axis(xmin=-l1 - l2, xmax=l1 + l2, ymin=-l1 - l2, ymax=l1 + l2)
        # plt.show()
        plt.pause(5)  # A pause to have some time to take screenshot or analyse data.
        plt.ioff()
    #plt.show(block=True)


def plotSpeed(l1, l2, real, expected, timer, timee ):
    l1, l2 = l1 / 100, l2 / 100
    deg = (2*np.pi)/360.0
    real, expected = real*deg, expected*deg
    speed12, speed11, speed21, speed22 = [], [], [], []
    def calJacobian(theta1, theta2):
        jacobian = [[-l1 * np.sin(theta1) - l2 * np.sin(theta1 + theta2), -l2 * np.sin(theta1 + theta2)],
                [l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2), l2 * np.cos(theta1 + theta2)]]
        jacobian = np.array(jacobian)
        return jacobian
    for i in real:
        angSpeed = np.array([[i[2]], [i[3]]])
        jaco1 = calJacobian(i[0], i[1])
        # jaco = jaco1 * angSpeed
        jaco = np.matmul(jaco1, angSpeed)
        linearSpeed = np.sqrt(jaco[1][0] ** 2 + jaco[1][0] ** 2)
        speed11.append(linearSpeed)
    for i in expected:
        angSpeed = np.array([[i[2]], [i[3]]])
        jaco1 = calJacobian(i[0], i[1])
        jaco = jaco1 * angSpeed
        linearSpeed = np.sqrt(jaco[0][0] ** 2 + jaco[1][0] ** 2)
        speed21.append(linearSpeed)
    plt.figure(2)
    plt.clf()
    plt.ion()
    start = 2
    # plt.plot(timer[start:], speed11[start:], timer[start:], speed12[start:], '-', color='red')
    plt.plot(timer[start:], speed11[start:], '-', color='red', label='Real Speed')
    # plt.plot(timee[start:], speed21[start:], timee[start:], speed22[start:], '-', color='blue')
    plt.plot(timee[start:], speed21[start:], '-', color='blue', label='Expected Speed')
    plt.legend()
    plt.plot()
    #plt.show()
    #plt.pause(0.1)





