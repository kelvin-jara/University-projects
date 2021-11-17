import roboticstoolbox as rtb
import spatialmath as sp
import numpy as np
import serial
import time


class RobotPositionerSecond():
    def __init__(self):
        self.robot = rtb.models.DH.Planar2()
        self.robot.links[0].a = 24
        self.robot.links[1].a = 21.5
        print("initial angles: ", self.robot.q)
        self.positions = []
        self.angles = []
        self.xP = 45.4
        self.yP = 0
        self.gain = 2
        self.interval = 0.01
        #self.arduino = serial.Serial('COM5', 115200, timeout=.1)
        self.msg = ""
        self.arduino = serial.Serial('COM5', 115200, timeout=.1)
        #self.y = threading.Thread(target=self.serialRobot)
        #self.y.start()


    def addPosition(self, l1, l2):
        self.positions.append(l1)
        self.positions.append(l2)

    def running(self):
        lastq = self.robot.q
        lastp = [ self.xP, self.yP]
        magnet = 1
        while True:
            if len(self.positions) > 0:
                cordinates = self.positions.pop(0)
                self.msg = str(cordinates[0]) + " : " + str(cordinates[1])
                print("COORDINATES TO GO: ",cordinates[0], " : ", cordinates[1])
                T = sp.SE3(cordinates[0], cordinates[1], 0)
                sol = self.robot.ikine_LM(T, mask = [1, 1, 0, 0, 0, 0]).q
                # qt = rtb.jtraj(lastq, sol, 20)
                # qt = rtb.mtraj(rtb.tpoly, lastq, sol, 20)
                qt = np.array(self.two_joint_arm(GOAL_TH=0.5, theta1=lastq[0], theta2=lastq[1] ,xin = cordinates[0], yin = cordinates[1]))
                # qt = rtb.mtraj(rtb.lspb,lastq, sol, 20)
                # print("Solution LM : ", '\n', sol, '\n', T)
                print(qt)
                self.robot.plot(qt, block=False, jointaxes=True, shadow=True)
                # actual = self.robot.fkine(qt.y[-1])
                # print("actual : ", '\n', actual)
                start_time = time.time()
                last_time = 0
                counter = 0
                if magnet == 0:
                    magnet = 1
                elif magnet == 1:
                    magnet = 0
                # arduino = serial.Serial('COM5', 115200, timeout=.1)
                time.sleep(1)  # give the connection a second to settle
                while counter < len(qt):
                    current_time = time.time()
                    diff = current_time - last_time
                    if diff > 0.08:
                        deg1 = -qt[counter][0] * (360.0 / (2 * np.pi))
                        deg2 = qt[counter][1] * (360.0 / (2 * np.pi))

                        # while True:
                        # msg = '#' + str(deg1) + ":" + str(deg2) + '#'
                        msg = '#' + str(9.99) + ":" + str(deg1) + ":" + str(deg2)+ ":" + str(magnet)  + '#'
                        # print(msg)
                        this = str.encode(str(msg))
                        self.arduino.write(this)
                        data = self.arduino.readline()
                        if data:
                            print( 'sent   ', msg, ' received:   ',data.decode())
                            pass
                        time.sleep(0.000001)

                        last_time = current_time
                        counter += 1
                now = True
                while True:
                    data = self.arduino.readline()
                    current_time = time.time()
                    diff = current_time - last_time
                    if data:
                        print(data)
                        pass
                    else :
                        if now:
                            last_time = current_time
                            now = False
                        if  diff > 5:
                            print('ready for next')
                            break

                # print("done ------")

                lastq = sol
                lastp = [cordinates[0], cordinates[1]]

    def serialRobot(self):

        while True:
            self.arduino.write(str.encode(self.msg))
            data = self.arduino.readline()
            if data:
                #print(data.decode())
                pass

    def ang_diff(self, theta1, theta2):
        # Returns the difference between two angles in the range -pi to +pi
        return (theta1 - theta2 + np.pi) % (2 * np.pi) - np.pi

    def two_joint_arm(self, GOAL_TH=0.0, theta1=0.0, theta2=0.0, xin = 0.0, yin = 0.0):
        """
        Computes the inverse kinematics for a planar 2DOF arm
        When out of bounds, rewrite x and y with last correct values
        """
        Kp, dt = self.gain, self.interval
        l1 = self.robot.links[0].a
        l2 = self.robot.links[1].a
        self.angles = []
        lastT1 = -10000
        lastT2 = -10000
        x, y = xin, yin
        x_prev, y_prev = None, None

        while True:
            try:
                if x is not None and y is not None:
                    x_prev = x
                    y_prev = y
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
                if theta1_goal < 0:
                    theta2_goal = -theta2_goal
                    tmp = np.math.atan2(l2 * np.sin(theta2_goal),
                                        (l1 + l2 * np.cos(theta2_goal)))
                    theta1_goal = np.math.atan2(y, x) - tmp

                theta1 = theta1 + Kp * self.ang_diff(theta1_goal, theta1) * dt
                theta2 = theta2 + Kp * self.ang_diff(theta2_goal, theta2) * dt


            except ValueError as e:
                print("Unreachable goal" + e)
            except TypeError:
                x = x_prev
                y = y_prev

            wrist = self.plot_arm(theta1, theta2, x, y)
            df1, df2 = theta1 - lastT1, theta2 - lastT2
            # check goal
            d2goal = None
            if x is not None and y is not None:
                d2goal = np.hypot(wrist[0] - x, wrist[1] - y)
            # print(d2goal)
            if abs(d2goal) < GOAL_TH and x is not None:
                print("coming with distace: ", df2)
                return self.angles
            elif  abs(df1) < 0.001 and abs(df2) < 0.001:
                print("comong with thethas: ", theta1, theta2)
                return self.angles
            lastT1 = theta1
            lastT2 = theta2


    def plot_arm(self, theta1, theta2, target_x, target_y):  # pragma: no cover
        l1 = self.robot.links[0].a
        l2 = self.robot.links[1].a
        shoulder = np.array([0, 0])
        elbow = shoulder + np.array([l1 * np.cos(theta1), l1 * np.sin(theta1)])
        wrist = elbow + \
                np.array([l2 * np.cos(theta1 + theta2), l2 * np.sin(theta1 + theta2)])

        self.angles.append([theta1, theta2])
        return wrist