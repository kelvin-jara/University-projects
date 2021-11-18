import roboticstoolbox as rtb
import spatialmath as sp
import numpy as np
import threading
import serial
import time
import string
import matplotlib.pyplot as plt
import random
from definePathAcce import linePath, createPathAcceleartion, plotTrajectoryCable, getTrajectoryLengths

class RobotPositionerThird:
    def __init__(self):
        self.positions = []  # List to save the points where the robot will go
        self.xP = 0
        self.yP = 0
        self.obstacles = {}
        self.msg = ""
        # create a serial object for the arduino microcontroller
        self.arduino = serial.Serial('COM5', 115200, timeout=.1)

    """ Adder of positions to the which the robot will go"""
    def addPosition(self, l1, l2):
        self.positions.append(l1)
        self.positions.append(l2)

    def running(self):
        lastq = np.array([[0, 0]])
        lastp = [ self.xP, self.yP]
        magnet = 1
        dragging = False
        do = True
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

                if not dragging:  # not objects avoidance
                    trj = linePath(lastp, cordinates)
                    dragging = True
                else: # if dragging a object, create a path with object avoidance
                    xObjects, yObjects = self.getObstacles()  # get the position of the objects
                    trj = createPathAcceleartion(xObjects, yObjects, lastp, cordinates)
                    dragging = False
                    print("I am avoiding obstables..")

                # inverse kinematics for the trajectory previously generated
                qt =  getTrajectoryLengths(45, lastq[-1][0], lastq[-1][1], trj)
                # plotTrajectoryCable(reach, lastp, cordinates, trj)

                print("Trajectory generated...: " + "\n" )
                timev, timevr = 0, 0
                last_time = 0
                counter = 0

                if magnet == 0:
                    magnet = 1
                elif magnet == 1:
                    magnet = 0
                time.sleep(1)  # give the connection a second to settle
                send = True
                received, speedReal, speedExpected, timer, timee = [], [], [], [], []
                start_time = time.time()
                while counter < len(qt) and send:
                    current_time = time.time()-start_time
                    diff = current_time - last_time
                    """This variable affects the speed of the robot"""
                    step = 0.04  # rate to send data to the arduino. Minimum 0.02.

                    if diff >= step:
                        l1, l2, l3, l4 = qt[counter][0], qt[counter][1], qt[counter][2], qt[counter][3]
                        milimiters = 10.0
                        l1, l2, l3, l4 = l1*milimiters, l2*milimiters, l3*milimiters, l4*milimiters
                        # message send to arduino
                        msg = '#' + str(9.99) + ":" + str(l1) + ":" + str(l2)+ ":" + str(l3)+ ":" + str(l4)+ ":" + str(magnet)  + '#'
                        # print(msg)
                        this = str.encode(str(msg))
                        timev += diff
                        timee.append(timev)
                        self.arduino.write(this) #  send lengths of robot through serial communication
                        data = self.arduino.readline()  # read data sent from arduino
                        if data:
                            gotten = data.decode()
                            # print(gotten)
                        time.sleep(0.000001)
                        last_time = current_time
                        counter += 1
                if send:
                    print(f"time to send:{str(time.time() - start_time)} and speed:{str(length / timee[-1])}")

                lastq = qt
                lastp = cordinates

    """Add obstacles to the list of obstacles"""
    def addObstacles(self, dic):
        self.obstacles = dic

    def getObstacles(self):
        obstaclesX, obstaclesY = [], []
        for i in self.obstacles.values():
            obstaclesX.append(i[0]), obstaclesY.append(i[1])

        return obstaclesX, obstaclesY

    def homing(self):
        l1, l2, l3, l4 = 0,0,0,0
        # message send to arduino
        msg = '#' + str(9.99) + ":" + str(l1) + ":" + str(l2) + ":" + str(l3) + ":" + str(l4) + ":" + str(magnet) + '#'
        this = str.encode(str(msg))
        self.arduino.write(this)



