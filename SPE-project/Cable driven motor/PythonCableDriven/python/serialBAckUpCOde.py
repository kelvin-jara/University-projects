
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
            theta1_goal = np.math.atan2(y, x) + tmp
        if not math.isnan(theta1_goal) and  not math.isnan(theta1_goal):

            pi = np.pi
            if counter == 0:
                counter += 1
            angle  = [theta1 - ang_diff(theta1, theta1_goal), theta2 - ang_diff(theta2, theta2_goal)]
            thetas.append(angle)
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