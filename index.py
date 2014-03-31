#!/usr/bin/python 
#coding=utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import os.path
import pymongo

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
                (r"/", IndexHandler),
                (r"/draw", DrawHandler),
                (r"/clear", clear),
                ]
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                debug=True,
                )
        conn = pymongo.Connection("localhost",27017)
        self.db = conn["yichuan"]
        tornado.web.Application.__init__(self,handlers,**settings)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class DrawHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            timestamp = int(self.get_argument('t'))
        except :
            timestamp = 0
        coll = self.application.db.draw
        drawLine = coll.find({"timestamp":{"$gt":timestamp}}).limit(100).sort("timestamp")
        print drawLine.count()
        data = []
        for line in drawLine:
            print line
            del line['_id']
            data.append(line)
        self.write(tornado.escape.json_encode(data))

class clear(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.draw
        coll.remove()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
