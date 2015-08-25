__author__ = 'jieli'

import sys
basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)
from modules import FtpServer

if __name__ == '__main__':

    HOST, PORT = "", 9002

    server = FtpServer.SocketServer.ThreadingTCPServer((HOST, PORT), FtpServer.MyTCPHandler)

    server.serve_forever()