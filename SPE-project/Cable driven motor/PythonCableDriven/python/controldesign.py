import roboticstoolbox as rtb
import spatialmath as sp
import PythonRobotics
import numpy as np
import threading
import serial
import time
import string
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


ti = np.linspace(0, 20, 500)
f = 20
deg1p = 90*np.sin(ti*2*np.pi/f)
deg2p = []
input = []
#plt.plot(ti, deg1p)
#print(deg1p)
#plt.tight_layout()
#plt.show()
start_time = time.time()
last_time = 0
counter = 0
arduino = serial.Serial('COM5', 115200, timeout=.1)
time.sleep(1)  # give the connection a second to settle
counter = 0
ib,tb, xb, yb = [], [], [], []
ti = 0
while ti < 1000:
    current_time = time.time()
    diff = current_time - last_time
    l = True
    if diff > 0.0001:
    #if l:
        f = 20
        #deg1 = np.sin(np.pi*current_time/f)*90
        #deg2 = np.sin(current_time)*90
        #input.append(deg1)
        #deg1 = deg1p[counter]
        #deg2 = deg1p[counter]
        ti = current_time - start_time
        deg1 = 90*np.sin(ti*2*np.pi/f)
        #if ti > 3:
        #    deg1 = 90
        deg2 = deg1
        msg = '#' + str(9.99) + ":" + str(-deg1) + ":" + str(deg2) + '#'
        # msg = int(deg1)
        # print(msg)
        this = str.encode(str(msg))
        arduino.write(this)
        time.sleep(0.00001)
        last_time = current_time
        counter += 1
    data = arduino.readline()
    if data:
        coming = data.decode(encoding='UTF-8',errors='ignore')
        # print(coming)
        msgb = coming.split(" ::: ")
        ib.append(deg1)
        tb.append(ti)
        xb.append(float(msgb[0]))
        yb.append(float(msgb[1].split("\r")[0]))
        #deg1p.append(float(coming[1]))
        #deg2p.append(float(coming[2]))
        print(msgb[0], msgb[1].split("\r")[0])

print(tb, '\n',xb, '\n', yb)

plt.plot(tb, xb, '-r')
plt.plot(tb, yb, '-g')
plt.plot(tb, ib, '-b')
plt.show()








"""
data = self.arduino.readline()
if data:
    print(data.decode())
"""

