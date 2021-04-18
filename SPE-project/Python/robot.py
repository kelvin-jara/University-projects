import roboticstoolbox as rtb
import spatialmath as sp
import PythonRobotics
import numpy as np
import threading


class RobotPositioner():
    def __init__(self):
        self.robot = rtb.models.DH.Planar2()
        self.robot.links[0].a = 2
        self.robot.links[1].a = 2
        self.positions = []


    def addPosition(self, l1, l2):

        self.positions.append(l1)
        self.positions.append(l2)

    def running(self):
        lastq = self.robot.q
        while True:
            if len(self.positions) > 0:
                cordinates = self.positions.pop(0)
                print(cordinates)
                T = sp.SE3(cordinates[0], cordinates[1], 0)
                sol = self.robot.ikine_min(T).q
                qt = rtb.jtraj(lastq, sol, 50)
                self.robot.plot(qt.y, block=False, jointaxes=True, shadow=True)
                print("done ------")
                lastq = sol


