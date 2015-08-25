#_*_coding:utf-8_*_
__author__ = 'jieli'
import SocketServer
import commands
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            self.data = self.request.recv(1024).strip() #接收客户端命令
            if not self.data :break
            print "{} wrote:".format(self.client_address[0])
            print self.data
            cmd_res = commands.getstatusoutput(self.data)
            # just send back the same data, but upper-cased
            msg_confirm = "MsgTransfer|SendReady|%s" % len(cmd_res[1])  #告诉客户端要发送多少数据给它
            self.request.send(msg_confirm)
            feedback = self.request.recv(100)  # 接收客户端的确认消息
            if feedback.startswith("MsgTransfer|RecvReady"): #判断客户端确认消息　

                self.request.sendall(cmd_res[1]) # 把命令结果全部发送给客户端
            else:
                print "---something wrong with the client side,because didn't recv the feedback from client..."

HOST, PORT = "", 9999
# Create the server, binding to localhost on port 9999
server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()
