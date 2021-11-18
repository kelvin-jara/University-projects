import socket
import threading
from robot import RobotPositioner
from robot2 import RobotPositionerSecond
from robot3 import RobotPositionerThird
from cameraStuff.camara2 import Camara
import time


def socketR(positioner):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    port = 12345
    s.bind(('127.0.0.1', port))
    print("socket binded to %s" % (port))
    print(s.family, s.type, s.proto)
    s.listen(5)
    print("socket is listening")
    c, addr = s.accept()
    print('Got connection from', addr)
    msg = 'Thank you for connecting'
    c.send(msg.encode("UTF-8"))
    camera = Camara()

    y = threading.Thread(target=sendSocekt, args=(c, camera,))
    y.start()
    y = threading.Thread(target=camera.get_Feed)
    y.start()
    dic = {}
    while True:
        b = c.recv(1024)
        string = b.decode("utf-8")

        fstring = string.split(" ? ")
        for i in range(len(fstring)):
            spliting = fstring[i].split(" : ")
            if len(spliting) == 3:
                x = spliting[1]
                y = spliting[2]
                id = spliting[0]
                if id in dic:
                    last = dic[id]

                    list = [float(x), float(y)]
                    if not list == last:
                        positioner.addPosition(last, list)
                        dicCopy = dict(dic)
                        dicCopy.pop(id)
                        positioner.addObstacles(dicCopy)
                        dic[id] = list
                    else:
                        pass
                else:

                    dic[id] = [float(x), float(y)]
    c.close()

def sendSocekt(c, camera):
    while True:
        dict = camera.get_objects()
        # camera reads = 38.0 and 47.0
        # we are using to match unity scale
        factorX, factorY = (750.0/camera.pixelsX), (927.0/camera.pixelsY)
        for i in dict:
            msg = i+":"+str(dict[i][0]*factorX)+":"+str(dict[i][1]*factorY)+"\n"
            c.send(msg.encode("UTF-8"))
            time.sleep(0.00001)



def program():
    positioner = RobotPositionerThird()
    x = threading.Thread(target=socketR, args=(positioner,))
    x.start()
    positioner.running()



program()