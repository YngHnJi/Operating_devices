# socket_server.py

# Server Part
# Reference: https://lidron.tistory.com/44

import socketserver
import threading

HOST = '210.123.42.42'
PORT = 5051
NUM_DEVICE = 0
lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성

class UserManager:
    def __init__(self):
        self.users = {} # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

    def addUser(self, username, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
        if username in self.users: # 이미 등록된 사용자라면
            conn.send('Already registered Device\n'.encode())
            return None

        # 새로운 사용자를 등록함
        lock.acquire() # 스레드 동기화를 막기위한 락
        self.users[username] = (conn, addr)
        lock.release() # 업데이트 후 락 해제

        self.sendMessageToAll('[%s] Connected to Server' %username)
       
        return username

    def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
        if msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
            #self.sendMessageToAll('[%s] %s' %(username, msg))
            self.sendMessageToAll(msg)
            return

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


# class react when request comes from client
class TCPHandler(socketserver.BaseRequestHandler):
    userman = UserManager()
   
    def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] Connected' %self.client_address[0])

        try:
            username = self.registerUsername()
            print("Num Devices Connected [%d / %d]" %(len(self.userman.users), NUM_DEVICE))

            if(len(self.userman.users) == NUM_DEVICE):
                print("All devices ready to be operated")
                while True:
                    msg = input("Type the command: ")
                    if(not msg):
                        ####### try to get input one more
                        print("Check the command provided")
                        while(msg):
                            msg = input("ReType the command: ")
                    elif(msg == "quit"):
                        print('===> Closing operating system.')
                        print('===> Type Ctrl+C to end the System.')
                        return
                    print(msg)

                    # Handle 
                    self.userman.messageHandler(username, msg)
            else:
                msg = self.request.recv(1024)
        except Exception as e:
            print(e)

    def registerUsername(self):
        while True:
            #self.request.send('Device ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class OperatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
       
def runServer():
    print('===> Start Device Operating System.')
    print('===> Type Ctrl+C to end the System.')

    try:
        socketserver.TCPServer.allow_reuse_address = True
        server = OperatingServer((HOST, PORT), TCPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

    print("\n===> Server Shutting down")

if __name__=="__main__":
    NUM_DEVICE = int(input("Type num of Devices you operate: "))

    runServer()
