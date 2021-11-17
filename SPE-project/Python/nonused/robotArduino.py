import roboticstoolbox as rtb
import spatialmath as sp
import numpy as np

robot = rtb.models.DH.Planar2()
robot.links[0].a = 20
robot.links[1].a = 21.5

positions = []
# arduino = serial.Serial('COM5', 115200, timeout=.1)
msg = ""

init = [35.5, 0]
final = [-10, 15.5]
final2 = [20, 30]
# final = [0, 35.5]
Lenght = np.sqrt((init[0] - final[0])**2 + (init[1] - final[1])**2)
N = 20
T = sp.SE3(init[0], init[1], 0)
T2 = sp.SE3(final[0], final[1], 0)
T3 = sp.SE3(final2[0], final2[1], 0)
sol = robot.ikine_LM(T,mask = [1, 1, 0, 0, 0, 0])
sol2 = robot.ikine_LM(T2,mask = [1, 1, 0, 0, 0, 0])
sol3 = robot.ikine_LM(T3,mask = [1, 1, 0, 0, 0, 0])
listofpoints = np.array([[sol.q[0],sol.q[1]], [sol2.q[0],sol2.q[1]], [sol3.q[0],sol3.q[1]]])
# print(listofpoints)
qt = rtb.jtraj(sol.q, sol2.q, N)
# qt = rtb.mtraj(rtb.lspb, sol.q, sol2.q, N)
# qt = rtb.mstraj(listofpoints,dt=0.01, tacc=0.1,qdmax=9)
#print("points: ", "\n", qt.q)
#qt = robot.jtraj(T, T2, N)
print(type(qt.y))
r = robot.plot(qt.y, block=True, jointaxes=True, shadow=True)
"""
#print(qt.y*360.0/(2*np.pi))
actual = robot.fkine(qt.y[-1])
print("solution: ", sol2, "\n", "should be: ", final,"\n", "currently is: ", "\n", actual)
"""
"""
print("actual : ", '\n', actual)
for i in range(1, len(qt.x)):
    dif = qt.x[i] - qt.x[i-1]
    # print(dif)


start_time = time.time()
last_time = 0
counter = 0
arduino = serial.Serial('COM5', 115200, timeout=.1)
time.sleep(1)  # give the connection a second to settle
while counter < len(qt.y):
    current_time = time.time()
    diff = current_time - last_time
    l = True
    #if diff > 0.01:
    if l:
        deg1 = qt.y[counter][0]*(360.0/(2*np.pi))
        deg2 = qt.y[counter][1]*(360.0/(2*np.pi))

        # while True:
        msg = '#' + str(deg1) + ":" + str(deg2) + '#'
        # print(msg)
        this = str.encode(str(msg))
        arduino.write(this)
        data = arduino.readline()
        if data:
            print(data)
            pass
        time.sleep(0.00001)

        last_time = current_time
        counter += 1
print("I am entering" )

while True:
    data = arduino.readline()
    if data:
        print(data)
        pass





"""

"""
data = self.arduino.readline()
if data:
    print(data.decode())
"""

