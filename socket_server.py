# socket_server.py

# temp1.py
# Server Part

import socketserver
import threading

HOST = '210.123.42.42'
PORT = 5050
NUM_DEVICE = 0
lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성

class UserManager: # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
  # ① 채팅 서버로 입장한 사용자의 등록
  # ② 채팅을 종료하는 사용자의 퇴장 관리
  # ③ 사용자가 입장하고 퇴장하는 관리
  # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송

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
        #print('+++ 대화 참여자 수 [%d]' %len(self.users))
       
        return username

    def removeUser(self, username): #사용자를 제거하는 함수
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s]님이 퇴장했습니다.' %username)
        #print('--- 대화 참여자 수 [%d]' %len(self.users))

    def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
        if msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
            #self.sendMessageToAll('[%s] %s' %(username, msg))
            self.sendMessageToAll(msg)
            return

        if msg.strip() == '/quit': # 보낸 메세지가 'quit'이면, stop program
            self.removeUser(username)
            return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


# class react when request comes from client
class TcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()
   
    def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
        print('[%s] 연결됨' %self.client_address[0])

        try:
            username= self.registerUsername()
            print("Devices Connected [%d / %d]" %(len(self.userman.users), NUM_DEVICE))

            if(len(self.userman.users) == NUM_DEVICE):
                print("All devices ready to be operated")
                msg = input("Type the command: ")
                # ===========> if msg not appropriate, get again
                while msg:
                    # ===> Put msg input in here for while loop
                    # if msg not in the list, type input again

                    print(msg)
                    self.userman.messageHandler(username, msg)

                    #echo_msg = self.request.recv(1024)
                    msg = input("Type the command: ")

            else:
                msg = self.request.recv(1024)

               
        except Exception as e:
            print(e)

        #print('[%s] 접속종료' %self.client_address[0])
        #self.userman.removeUser(username)

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
        server = OperatingServer((HOST, PORT), TcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- Close operating system.')
        server.shutdown()
        server.server_close()


if __name__=="__main__":
    NUM_DEVICE = int(input("Type num of Devices you run: "))

    runServer()