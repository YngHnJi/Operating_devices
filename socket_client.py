# socket_client.py

import socket
from threading import Thread

HOST = '210.123.42.42'
PORT = 5050
DEVICE_NAME = "DEVICE 1"

def rcvMsg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            elif(data.decode() == "quit"):
                break

            
            print(data.decode())
            # function(data.decode())
        except:
            pass

def runSys():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        init_id = DEVICE_NAME
        sock.send(init_id.encode())

        rcvMsg(sock)

    print("===> Client System closed")

if __name__=="__main__":
    runSys()
