#!/usr/bin/env python

from SocketServer import(ThreadingTCPServer as TCP,StreamRequestHandler as SRH)
from time import ctime
import time
import traceback
import pymongo

HOST = ''
PORT = 10086
ADDR = (HOST, PORT)
conn = pymongo.Connection("localhost",27017)
db = conn["yichuan"]

class MyRequestHandler(SRH):
    def handle(self):
        while True:
            timestamp = int(time.time())
            try:
                data = self.rfile.readline().strip().split(',')
                coll  = db.draw
                draw_line = {'timestamp':timestamp,'line':{'x1':int(data[0]),'y1':int(data[1]),\
                        'x2':int(data[2]),'y2':int(data[3])}}
                coll.insert(draw_line)
                print timestamp,self.client_address,draw_line
            except :
                print "break"
                traceback.print_exc()
                break

TCP.allow_reuse_address = True
tcpServ = TCP(ADDR,MyRequestHandler)
print 'waitting for connection..'
tcpServ.serve_forever()
