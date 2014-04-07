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
                coll = db.AIid
                new_id = coll.find_and_modify(update={"$inc":{"timestamp":1}}, new=True).get("timestamp")
                coll  = db.draw
                if data[0]=='d':
                    draw_line = {'timestamp':new_id,'type':'draw','file_id':int(data[5]),'line':{'x1':int(data[1]),'y1':int(data[2]),\
                        'x2':int(data[3]),'y2':int(data[4])}}
                elif data[0]=='j':
                    draw_line = {'timestamp':new_id,'type':'jump','file_id':int(data[2]),'page':int(data[1])}
                coll.insert(draw_line)
            except :
                print "break"
                traceback.print_exc()
                break

TCP.allow_reuse_address = True
tcpServ = TCP(ADDR,MyRequestHandler)
print 'waitting for connection..'
tcpServ.serve_forever()
