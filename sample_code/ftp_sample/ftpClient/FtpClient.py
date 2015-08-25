#_*_coding:utf-8_*_
__author__ = 'jieli'

# Echo client program
import socket
import os
class FtpClient(object):
    def __init__(self,host,port ):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
    def start(self):
        self.interactive()
    def interactive(self):
        while True:
            user_input = raw_input(">>:").strip()
            if len(user_input) == 0:continue
            user_input = user_input.split()

            if hasattr(self,user_input[0]):
                func = getattr(self,user_input[0])
                func(user_input)

            else:
                print "\033[31;1mWrong cmd usage\033[0m"

    def get(self,msg):
        print '--get func---',msg
        if len(msg) ==2 :
            file_name = msg[1]
            instruction = "FileTransfer|get|%s" % file_name
            self.sock.send(instruction)
            feedback = self.sock.recv(100)
            print '-->',feedback
            if feedback.startswith("FileTransfer|get|ready"):
                file_size = int(feedback.split("|")[-1])
                self.sock.send("FileTransfer|get|recv_ready")
                recv_size = 0
                f = file('client_recv/%s' % os.path.basename(file_name),'wb')
                print '--->',file_name
                while not file_size == recv_size:
                    if file_size - recv_size>1024:
                        data = self.sock.recv(1024) #actual receive may less than 1024
                        recv_size += len(data)
                    else:# less than 1024
                        data = self.sock.recv(file_size - recv_size)
                        recv_size += (file_size - recv_size)
                    f.write(data)
                    print file_size,recv_size
                else:
                    print '---recv file:%s---' % file_name
                    f.close()
            else:
                print feedback
        else:
            print "\033[31;1mWrong cmd usage\033[0m"

    def put(self):
        pass
    def ls(self):
        pass
    def cd(self):
        pass
    def delete(self):
        pass


if __name__ == "__main__":
    f = FtpClient('localhost',9002)
    f.start()