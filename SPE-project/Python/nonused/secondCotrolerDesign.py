import numpy as np
import serial
import time

ti = np.linspace(0, 20, 500)
f = 10
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
while ti < 20:
    current_time = time.time()
    diff = current_time - last_time
    l = True
    if diff > 0.0001:
    #if l:
        f = 10
        #deg1 = np.sin(np.pi*current_time/f)*90
        #deg2 = np.sin(current_time)*90
        #input.append(deg1)
        #deg1 = deg1p[counter]
        #deg2 = deg1p[counter]
        ti = current_time - start_time
        deg1 = round(20*np.sin(ti*2*np.pi/f), 2)
        #if ti > 3:

        deg2 = deg1
        msg = '#' + str(9.99) + ":" + str(deg1) + ":" + str(deg2) + '#'
        #msg = '#' + "hello" + '#'
        #sg = str(deg1) + ":" + str(deg2)
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
        print(msg, "--", coming)
        #print(coming)







"""
data = self.arduino.readline()
if data:
    print(data.decode())
"""

