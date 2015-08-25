#_*_coding:utf-8_*_
__author__ = 'jieli'


import socket
import sys,os
import getpass






class Client(object):

    func_dic = {
        'help': 'help',
        'get' : 'get_file',
        'put' : 'put_file',
        'exit': 'exit',
        'ls'  : 'list_file',
        'cd'  :  'switch_dir',
        'del' :  'delete'
    }
    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))
        self.exit_flag = False
        if self.auth():

            self.interactive()

    #def msg_wrapper(self,*args):
    def list_file(self,msg):
        #print '---list file---',msg

        instruction = "list_file|%s" %(' '.join(msg[1:]))
        self.sock.send(instruction)
        server_confirm_msg = self.sock.recv(100)
        if server_confirm_msg.startswith("message_transfer::ready"):
            server_confirm_msg = server_confirm_msg.split("::")
            msg_size = int(server_confirm_msg[-1])
            self.sock.send("message_transfer::ready::client")
            recv_size = 0
            while not msg_size == recv_size:
                if msg_size - recv_size > 1024:
                    data = self.sock.recv(1024)

                else:
                    data = self.sock.recv(msg_size - recv_size)
                recv_size += len(data)
                sys.stdout.write(data)
    def switch_dir(self,msg ):
        #print '--swtich dir:',msg
        self.sock.send("switch_dir|%s"  % ' '.join(msg))
        feedback = self.sock.recv(100)
        #print '==>',feedback
        if feedback.startswith("switch_dir::ok"):
            self.cur_path  = feedback.split("::")[-1]
        else:
            print "\033[31;1m%s\033[0m" % feedback.split("::")[-1]
    def delete(self,msg):
        if len(msg) > 1:
            instruction = "delete_file|%s" % ' '.join(msg[1:])
            self.sock.send(instruction)

        else:
            print "\033[31;1mWrong command usage\033[0m"
    def auth(self):
        retry_count = 0
        while retry_count < 3:
            username = raw_input("username:").strip()
            if len(username) == 0:continue
            passwd = getpass.getpass()
            auth_str = "ftp_authentication|%s|%s" %(username,passwd)

            self.sock.send(auth_str)
            auth_feedback = self.sock.recv(1024)

            if auth_feedback == "ftp_authentication::success":
                print "\033[32;1mAuthentication Passed!\033[0m"
                self.username  = username
                self.cur_path = username
                return True
            else:
                print "\033[31;1mWrong username or password\033[0m"
                retry_count +=1
        else:
            print "\033[31;1mToo many attempts,exit!\033[0m"
    def interactive(self):
        '''allowcate task to different function according to msg type'''
        try:
            while not self.exit_flag:
                cmd = raw_input("[\033[;32;1m%s:\033[0m%s]>>:" % (self.username,self.cur_path) ).strip()
                if len(cmd) == 0:continue
                cmd_parse = cmd.split()
                msg_type = cmd_parse[0]
                #print 'msg_type::',msg_type
                if self.func_dic.has_key(msg_type):
                    func = getattr(self,self.func_dic[msg_type])
                    func(cmd_parse)
                else:
                    print "Invalid instruction,type [help] to see available cmd list"
        except KeyboardInterrupt:
            self.exit('exit')
        except EOFError:
            self.exit('exit')
    def put_file(self,msg):
        #print '---uploading file----',msg
        if len(msg) == 2:# put local_filename
            if os.path.isfile(msg[1]):

                file_size = os.path.getsize(msg[1])
                instruction_msg = "file_transfer|put|send_ready|%s|%s" %(msg[1],file_size)
                self.sock.send(instruction_msg)
                feedback = self.sock.recv(1024)
                print '==>',feedback
                progress_percent = 0
                if feedback.startswith("file_transfer::put_file::recv_ready"):
                    f = file(msg[1], "rb")
                    sent_size = 0
                    while not sent_size == file_size:
                        if file_size - sent_size <= 1024:
                            data = f.read(file_size - sent_size)
                            sent_size += file_size - sent_size
                        else:
                            data = f.read(1024)
                            sent_size += 1024
                        self.sock.send(data)
                        #print '-->',file_size,sent_size

                        cur_percent = int(float(sent_size) / file_size * 100)
                        if cur_percent > progress_percent:
                            progress_percent = cur_percent
                            self.show_progress(file_size,sent_size,progress_percent)
                    else:
                        print "--send file:%s done---" % msg[1]
                    f.close()

            else:
                print "\033[31;1mFile %s doesn't exist on local disk\033[0m" % msg[1]
    def get_file(self,msg):
        if len(msg) == 2: # get remote_filename
            msg = "file_transfer|get|%s" % msg[1]
            self.sock.send(msg)
            feedback = self.sock.recv(1024)
            if feedback.startswith('file_transfer::get_file::send_ready'):
                file_size = int(feedback.split("::")[-1])
                filename = os.path.basename(msg.split("|")[-1])
                #print 'filename:',filename, msg
                f = file(filename,'wb')
                #print "--going to recv", feedback
                self.sock.send('file_transfer::get_file::recv_ready')
                size_recv = 0
                progress_percent = 0
                while not size_recv == file_size:
                    data = self.sock.recv(file_size-size_recv)
                    size_recv += len(data)
                    f.write(data )

                    cur_percent = int(float(size_recv) / file_size * 100)
                    if cur_percent > progress_percent:
                        progress_percent = cur_percent
                        self.show_progress(file_size,size_recv,progress_percent)
                else:
                    print "recieved the file done"

            else:#file doesn't exist on remote or sth else went wrong.
                print '\033[31;1m%s\033[0m' %feedback
    def show_progress(self,total,finished,percent):

        progress_mark = "=" * (percent/2)
        sys.stdout.write("[%s/%s]%s>%s\r" %(total,finished,progress_mark,percent))
        sys.stdout.flush()
        if percent == 100:
            print '\n'
    def exit(self,msg):
        self.sock.shutdown(socket.SHUT_WR)
        sys.exit("Bye! %s" % self.username)
    def help(self,msg):
        print '''
        help    help
        get     get remote_filename
        put     put local_filename
        exit    exit the system
        ls      list all the files in current directory
        cd      cd some_dir
        del     del remote_filename
        '''
if __name__ == "__main__":
    #Host,Port = 'localhost', 9000
    s = Client('localhost', 9000)

