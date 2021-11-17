import socket

ip = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())
port = 12345

Server_address_family = (ip, port)  # server address family

try:
    client = socket.socket()
    client.connect(Server_address_family)
    print("python has already connect to C#")
    print("wait message from C#")
    while 1:
        msg = client.recv(1024)
        print(msg.decode())
except Exception as e:
    print(e)
    print("Connection failed...")