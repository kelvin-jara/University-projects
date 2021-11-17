# first of all import the socket library
import socket

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
                    dic[id] = list
                else:
                    pass
            else:

                dic[id] = [float(x), float(y)]
c.close()