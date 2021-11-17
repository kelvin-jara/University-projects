import numpy as np
import matplotlib.pyplot as plt
import time

def createPathAcceleartion(xPosObjects, yPosObjects, intiPos, finalPos):
    # Plot the objects position with a radius around them
    angle = np.linspace(0, 2 * np.pi)
    r = 0.2
    for i in range(len(xPosObjects)):
        x = xPosObjects[i] + r * np.cos(angle)
        y = yPosObjects[i] + r * np.sin(angle)
        plt.plot(x, y, '-', color='red')
    plt.plot(xPosObjects, yPosObjects, 'ro', color='green')

    xs, ys = [intiPos[0], finalPos[0]],[intiPos[1], finalPos[1]]
    print("debuging diff :",intiPos[0]-finalPos[0])
    # If the point are located in the same y-position, it means the slope if infinity and cn not be used
    # then just make points N points between the initial and final position
    if abs(intiPos[0]-finalPos[0]) < 1.0:
        trj = []
        for i in range(50):
            trj.append([intiPos[0], (i/50)*finalPos[1]])
        print("returning simple: ", trj)
        return trj
    # plot initial and final position
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
            # if the distance between the point in the line and the radius of the objects is then a threeshold,
            # it means the trajectory collides with radius of the objects
            if abs(difx)< 0.2 and abs(dify) < 0.2:
                if i not in xIntersec and j not in yIntersec:
                    # if collides then add the position of objects to a new list
                    xIntersec.append(i)
                    yIntersec.append(j)
                plt.plot(i, j, '.', color='yellow')
    pointsXmin, pointsXmax, pointsYmin, pointsYmax = [], [], [], []
    for i, j in zip(xIntersec, yIntersec):
        x = i + r * np.cos(angle) # obtain the x-points of the radius
        b2 = j - (-m) * i # draw a line perpendicular to straight trajectory
        y3, y4 = -m * min(x) + b2, -m * max(x) + b2
        pointsXmin.append(min(x)), pointsYmin.append(y3)
        pointsXmax.append(max(x)), pointsYmax.append(y4)
    plt.plot(pointsXmin, pointsYmin, 'o', color='red')
    # it is neccesary to order the colliding points
    # the sort fcntion is not enough fo this  case, so Dataframe makes it easy
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