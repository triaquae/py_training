#_*_coding:utf-8_*_
__author__ = 'jieli'
import SocketServer

import os
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            instruction = self.request.recv(1024).strip() #接收客户端命令
            if not instruction :break
            instruction = instruction.split('|')
            if hasattr(self,instruction[0]):
                func = getattr(self, instruction[0])
                func(instruction)
    def FileTransfer(self,msg):
        print '---filetransfer---',msg
        if msg[1] == 'get': #client downloads file from server
            print "client wants to download file:", msg[2]
            if os.path.isfile(msg[2]):
                file_size = os.path.getsize(msg[2])
                res = "ready|%s" % file_size
            else:
                res = "file doesn't exist"
            send_confirmation = "FileTransfer|get|%s" %res
            self.request.send(send_confirmation)
            feedback = self.request.recv(100)
            if feedback == 'FileTransfer|get|recv_ready':
                f = file(msg[2],'rb')
                send_size = 0
                while not file_size == send_size :
                    if file_size - send_size > 1024:
                        data = f.read(1024)
                        send_size += 1024
                    else: #left data less than 1024
                        data = f.read(file_size - send_size)
                        send_size +=(file_size - send_size)
                    self.request.send(data)
                    print file_size,send_size
                else:
                    print '---send file:%s done----' % msg[2]
                    f.close()
        elif msg[1] == 'put':
            pass


if __name__ == '__main__':

    HOST, PORT = "", 9002

    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    server.serve_forever()

