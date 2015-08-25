#_*_coding:utf-8_*_

import SocketServer
import account
import os,sys,commands
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    exit_flag = False
    def handle(self):
        # self.request is the TCP socket connected to the client

        while not self.exit_flag:
            msg = self.request.recv(1024)
            if not msg:
                break
            msg_parse = msg.split("|")
            msg_type = msg_parse[0]
            if hasattr(self,msg_type):
                #print "---allowcate msg to method %s ---" % msg_type,msg_parse
                func = getattr(self,msg_type)
                func(msg_parse)
            else:
                print "--\033[31;1mWrong msg type:%s\033[0m--" % msg_type
    def ftp_authentication(self,msg):
        #print '----auth----'
        auth_res = False
        if len(msg) == 3:
            msg_type,username,passwd = msg
            if account.accounts.has_key(username):
                if account.accounts[username]['passwd'] == passwd:
                    auth_res = True
                    self.login_user = username
                    self.cur_path = '%s/%s' %(os.path.dirname(__file__),account.accounts[username]['home'])
                    self.home_path = '%s/%s' %(os.path.dirname(__file__),account.accounts[username]['home'])
                else:
                    #print '---wrong passwd---'
                    auth_res = False
            else:
                auth_res == False
        else:
            auth_res == False

        if auth_res:
            msg = "%s::success" % msg_type
            print '\033[32;1muser:%s has passed authentication!\033[0m' % username

        else:
            msg = "%s::failed" % msg_type
        self.request.send(msg)
    def has_privilege(self,path):
        abs_path = os.path.abspath(path)
        if abs_path.startswith(self.home_path):
            return True
        else:
            return  False
    def file_transfer(self,msg):
        #print msg
        transfer_type = msg[1]
        filename = '%s/%s' %(self.cur_path,msg[2])
        self.has_privilege(filename)
        if transfer_type == 'get': #download from server
            if os.path.isfile(filename) and self.has_privilege(filename):

                file_size = os.path.getsize(filename)
                confirm_msg = "file_transfer::get_file::send_ready::%s" % file_size
                self.request.send(confirm_msg)
                client_confirm_msg = self.request.recv(1024)
                if client_confirm_msg == "file_transfer::get_file::recv_ready":
                    f = file(filename,'rb')
                    size_left = file_size
                    #print "--size left:",size_left
                    while size_left >0:
                        if size_left < 1024:
                            self.request.send(f.read(size_left))
                            size_left = 0
                        else:
                            self.request.send(f.read(1024))
                            size_left -= 1024

                    else:
                        print "send file done...."
            else:#file doesn't exist
                err_msg = "file_transfer::get_file::error::file does not exist or is a directory"
                self.request.send(err_msg)
        elif transfer_type == 'put':#upload file to server
            #print '-->', msg
            filename,file_size = msg[-2],int(msg[-1])
            filename = '%s/%s' %(self.cur_path,filename)
            print 'filename:',filename
            if os.path.isfile(filename):
                f = file('%s.0' % (filename),'wb')
            else:
                f = file("%s" %(filename) ,'wb')
            confirm_msg = "file_transfer::put_file::recv_ready"
            self.request.send(confirm_msg)
            recv_size = 0
            while not recv_size == file_size:
                data = self.request.recv(1024)
                recv_size += len(data)
                f.write(data)
            else:
                print "--\033[32;1mReceiving file:%s done\033[0m--" %(filename)
                #print len(file_content), file_content[-100:]
                f.close()
    def delete_file(self,msg):
        print '-->delete:',msg
        file_list = msg[1].split()
        res_list = []
        for i in file_list:
            abs_file_path = "%s/%s" %(self.cur_path,i)
            cmd_res = commands.getstatusoutput("rm -rf %s"% abs_file_path)[1]



    def list_file(self,msg):
        '''display file list'''
        home_prefix = account.accounts[self.login_user]['home']
        cmd = "cd %s;ls -lh %s"% (self.cur_path,' '.join(msg[1:]))
        file_list= os.popen(cmd).read()
        confirm_msg = "message_transfer::ready::%s" % len(file_list)
        self.request.send(confirm_msg)
        confirm_from_client = self.request.recv(100)
        if confirm_from_client == "message_transfer::ready::client":
            self.request.sendall(file_list)
    def switch_dir(self,msg):
        #print '---switch dir:', msg
        switch_res = ""
        msg = msg[-1].split()
        if len(msg) ==1:# means no dir follows cd cmd, go back to home directory
            self.cur_path = self.home_path
            relative_path = self.cur_path.split(self.home_path)[-1]
            switch_res = "switch_dir::ok::%s" % relative_path
        elif len(msg) == 2:
            if os.path.isdir("%s/%s" %(self.cur_path,msg[-1])):
                abs_path = os.path.abspath("%s/%s" %(self.cur_path,msg[-1]))
                if abs_path.startswith(self.home_path):#need to make user can only access to the home path level
                    self.cur_path = abs_path
                    relative_path = self.cur_path.split(self.home_path)[-1]
                    switch_res = "switch_dir::ok::%s" % relative_path
                else:
                    switch_res = "switch_dir::error::target dir doesn't exist"
            else:
                switch_res = "switch_dir::error::target dir doesn't exist"
        else:
            switch_res = "switch_dir::error::Error:wrong command usage."
        self.request.send(switch_res)
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()