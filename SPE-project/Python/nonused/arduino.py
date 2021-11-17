import serial
import time
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


arduino = serial.Serial('COM5', 115200, timeout=.1)
time.sleep(1)  # give the connection a second to settle

while True:
    msg = '#' + "12.56:11.45" + '#'
    this = str.encode(str(msg))
    arduino.write(this)
    data = arduino.readline()
    if data:
        print(data.decode())
    time.sleep(0.000001)