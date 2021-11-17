import roboticstoolbox as rtb
import numpy as np
import serial
import time
from definePathAcce import linePath, inverseGenerator, plotTrj, createPathAcceleartion

class RobotPositionerThird:
    def __init__(self):
        self.robot = rtb.models.DH.Planar2()
        self.robot.links[0].a = 24
        self.robot.links[1].a = 21.5
        print("initial angles: ", self.robot.q)
        self.positions = []
        self.angles = []
        self.angles = []
        self.xP = 45.49
        self.yP = 0
        self.obstacles = {}
        self.msg = ""
        self.arduino = serial.Serial('COM5', 115200, timeout=.1)


    def addPosition(self, l1, l2):
        self.positions.append(l1)
        self.positions.append(l2)

    def running(self):
        lastq = np.array([[0, 0]])
        lastp = [ self.xP, self.yP]
        l1, l2 = 24, 21.5
        magnet = 1
        dragging = False
        do = True
        lastheta1, lastheta2 = 0, 0
        while True :
            if len(self.positions) > 0 and do:
                cordinates = self.positions.pop(0)
                if cordinates == lastp:
                    if magnet == 0:
                        magnet = 1
                    elif magnet == 1:
                        magnet = 0
                    continue

                self.msg = str(cordinates[0]) + " : " + str(cordinates[1])
                print("COORDINATES TO GO: ",cordinates[0], " : ", cordinates[1])

                length = np.sqrt((lastp[0] - cordinates[0])**2 + (lastp[1] - cordinates[1])**2)/100
                print(f"distance is:{length}")

                if not dragging:
                    trj = linePath(lastp, cordinates)
                    dragging = True
                else:
                    xObjects, yObjects = self.getObstacles()
                    trj = createPathAcceleartion(xObjects, yObjects, lastp, cordinates)
                    dragging = False
                    print("I am avoiding obstables..")

                qt = inverseGenerator(trj, lastq[-1][0], lastq[-1][1])
                plotTrj(qt, 24, 21.5)
                # print(f"last_qt:{lastq[-1]} and qt:{qt}")
                print("Trajectory generated...: ")
                timev, timevr = 0, 0
                last_time = 0
                counter = 0
                if magnet == 0:
                    magnet = 1
                elif magnet == 1:
                    magnet = 0
                time.sleep(1)  # give the connection a second to settle
                send = True  # bool to send or not commands to the Arduino
                received, speedReal, speedExpected, timer, timee = [], [], [], [], []
                lastdeg1, lastdeg2 = 0, 0
                lastdegReal1, lastdegReal2 = 0, 0
                start_time = time.time()
                while counter < len(qt) and send:
                    current_time = time.time()-start_time
                    diff = current_time - last_time
                    step = 0.01
                    if diff >= step:
                        deg1 = -qt[counter][0] * (360.0 / (2 * np.pi))
                        deg2 = qt[counter][1] * (360.0 / (2 * np.pi))
                        msg = '#' + str(9.99) + ":" + str(deg1) + ":" + str(deg2)+ ":" + str(magnet)  + '#'
                        msgToPrint = '#' + str(deg1) + ":" + str(deg2)+ ":" + str(magnet)  + '#'
                        this = str.encode(str(msg))
                        num1,  num2 = deg1 - lastdeg1, deg2 - lastdeg2
                        timev += diff
                        timee.append(timev)
                        speedExpected.append([deg1, deg2, num1/step, num2/step])
                        lastdeg1, lastdeg2 = deg1, deg2
                        self.arduino.write(this)
                        data = self.arduino.readline()
                        limit = 10
                        if data:
                            gotten = data.decode()
                            num = gotten.split(" ::: ")
                            currentOne, currentTwo = -float(num[0]), float(num[1])
                            diff1, diff2 = currentOne - lastdegReal1, currentTwo - lastdegReal2
                            lastdegReal1, lastdegReal2 = currentOne, currentTwo
                            received.append([currentOne, currentTwo])
                            timevr += diff
                            timer.append(timevr)
                            speedReal.append([currentOne, currentTwo, diff1/step, diff2/step])
                        time.sleep(0.000001)
                        last_time = current_time
                        counter += 1
                if send:
                    """
                    unccoment the lines below if plots are desied to show
                    speed and trajectory followed by the robot"""
                    #plotTrj(np.array(received), l1, l2, endeffector=True, real=qt)
                    #plotSpeed(l1, l2, np.array(speedReal), np.array(speedExpected), timer, timee)
                    print(f"time to send:{str(time.time() - start_time)} and speed:{str(length / timee[-1])}")
                now = True
                lastq = qt
                lastp = cordinates


    def addObstacles(self, dic):
        self.obstacles = dic

    def getObstacles(self):
        obstaclesX, obstaclesY = [], []
        for i in self.obstacles.values():
            obstaclesX.append(i[0]), obstaclesY.append(i[1])

        return obstaclesX, obstaclesY



