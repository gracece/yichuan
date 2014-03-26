#!/usr/bin/env python

from SocketServer import(ThreadingTCPServer as TCP,StreamRequestHandler as SRH)
from time import ctime
import time
import traceback

HOST = ''
PORT = 10086
ADDR = (HOST, PORT)

class MyRequestHandler(SRH):
    def handle(self):
        while True:
            timestamp = int(time.time())
            try:
                data = self.rfile.readline().strip().split(',')
                print timestamp,self.client_address,data
                record = '{"x1":%s,"y1":%s,"x2":%s,"y2":%s}'%(data[0],data[1],data[2],data[3])
                fp = open('./line.txt','a')
                fp.write(str(timestamp)+'#'+record+'\n')
            except :
                print "break"
                traceback.print_exc()
                break

tcpServ = TCP(ADDR,MyRequestHandler)
tcpServ.allow_reuse_address=1
print 'waitting for connection..'
tcpServ.serve_forever()
