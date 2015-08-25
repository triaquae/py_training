#_*_coding:utf-8_*_
__author__ = 'jieli'

# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 9999             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    msg = raw_input("input:").strip()
    if len(msg) == 0:continue
    s.sendall(msg) # 发送具体命令
    server_confirm = s.recv(100) #接收服务器端接下来要发过来的数据包长度的消息
    if server_confirm.startswith("MsgTransfer|SendReady|"):
        msg_size = int(server_confirm.split("|")[-1]) #取出服务器端要响应的数据包的长度信息
        s.send("MsgTransfer|RecvReady") #给服务器端发送已经准备好接收命令结果的确认消息
        recv_data = ''
        recv_size = 0 #已收到数据
        while not msg_size == recv_size:# not done
            if msg_size - recv_size > 1024: # 还有好多数据没收回来
                data = s.recv(1024) #实际收到的可能比１０２４小
                recv_size += len(data)
            else:
                data = s.recv(msg_size - recv_size)
                recv_size += (msg_size - recv_size)
            recv_data +=data
            print '-->', msg_size,recv_size
        else:
            print recv_data
            print "----recv msg done----"



    print 'Received', data

s.close()