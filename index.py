#!/usr/bin/python 
#coding=utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import os.path

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class DrawHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            timestamp = self.get_argument('t')
        except :
            timestamp = 0
        fp = open("./line.txt","r")
        drawLine = []
        for line in fp:
            line.split("#")
            line = line.strip().split("#")
            if line[0]>=timestamp:
                data = dict()
                data['timestamp'] = line[0]
                data['line'] = tornado.escape.json_decode(line[1])
                print data
                drawLine.append(data)

        self.write(tornado.escape.json_encode(drawLine))

class clear(tornado.web.RequestHandler):
    def get(self):
        fp = open("./line.txt","w")



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/", IndexHandler),
        (r"/draw", DrawHandler),
        (r"/clear", clear),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
