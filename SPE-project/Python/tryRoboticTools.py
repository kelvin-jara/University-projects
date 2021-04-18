import roboticstoolbox as rtb
import spatialmath as sp
import PythonRobotics
import numpy as np
robot = rtb.models.DH.Planar2()
robot.links[0].a= 2; robot.links[1].a = 2

# print(robot.fkine([1, 34]))
# print(robot.r, "\n", robot.offset)
# print(robot.q)
t = np.linspace(0, 5, num=50)
s = np.linspace(1, 5, num=50)

# print(t)
# qo = np.ndarray((1, 2), buffer=np.array([0, 0]), offset=0, dtype=int)
#qf = np.ndarray((1, 2), buffer=np.array([1, 1]), offset=0, dtype=int)
#t = np.ndarray((1, 2), buffer=np.array([0, 1]), offset=0, dtype= int)
qo = float(0)
qf = float(3)
#t = 10
# print(qo, "\n", qf, "\n", t)
# rtb.jtraj(q0, qf, 3)
# robot.plot(robot.q)
# trj = rtb.jtraj()
"""
trj = rtb.tpoly(qo, qf, t, qd0=0, qdf=0)
print(trj.x,"\n", trj.y )
trj.plot( block=True, plotargs=None, textargs=None)
trj = rtb.lspb(qo, qf, t, V=None)
print(trj.x,"\n", trj.y )
trj.plot( block=True, plotargs=None, textargs=None)
"""
T = sp.SE3(2, -1, 0)
T2 = sp.SE3(-1, 3, 0)
#print(T)
sol = robot.ikine_min(T)
sol2 = robot.ikine_min(T2)
#print(sol)

q_pickup = sol.q
# print(robot.fkine(q_pickup))

qt = rtb.jtraj(robot.q, q_pickup, 50)


q0 = [0, 0]
q1 = sol.q
q2 = sol2.q
array = []
array.append(q0)
array.append(q1)
array.append(q2)
qs = np.array(array)
print("I am here", "\n",qs)

qtot = np.ndarray(shape = (3, 2), buffer=qs, dtype=float)
# print(q1, "\n", q2, "\n", qtot)
trj2 = rtb.tools.trajectory.mstraj(viapoints=qtot, dt=float(0.1), tacc=float(1), qdmax=3)
# print(trj2.q, "\n", qt)
robot.plot(trj2.q, movie="dhplanar22.gif", block=False)
print("Hello I am here")
