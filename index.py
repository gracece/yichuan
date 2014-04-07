#!/usr/bin/python 
#coding=utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import os.path
import os
import pymongo
from wand.image import Image
from wand.color import Color

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
                (r"/", IndexHandler),
                (r"/show/(\w+)", ShowHandler),
                (r"/draw", DrawHandler),
                (r"/clear", clear),
                (r"/list", list),
                (r"/upload", upload),
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
        coll = self.application.db.file
        filelist = coll.find()
        data = []
        for line in filelist:
            del line['_id']
            data.append(line)
        self.render("index.html",filelist=data)

class ShowHandler(tornado.web.RequestHandler):
    def get(self,show_id):
        coll = self.application.db.draw
        coll.remove({'file_id':show_id})
        coll = self.application.db.file
        fileinfo = coll.find_one({'file_id':show_id})
        self.render("show.html",file_id=show_id,fileinfo=fileinfo)

class DrawHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            timestamp = int(self.get_argument('t'))
            file_id = int(self.get_argument('f'))
        except :
            timestamp = 0
        coll = self.application.db.draw
        drawLine = coll.find({"timestamp":{"$gt":timestamp},"file_id":file_id}).limit(100).sort("timestamp")
        data = []
        for line in drawLine:
            print line
            del line['_id']
            data.append(line)
        self.write(tornado.escape.json_encode(data))

class list(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.file
        filelist = coll.find()
        data = []
        for line in filelist:
            del line['_id']
            data.append(line)
        self.write(tornado.escape.json_encode(data))

class clear(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.draw
        coll.remove()

class upload(tornado.web.RequestHandler):
    def get(self):
        self.render("upload.html")
    def post(self):
        coll = self.application.db.AIid
        new_id = str(int(coll.find_and_modify(update={"$inc":{"file":1}}, new=True).get("file")))
        upload_file = self.request.files['file'][0]
        upload_path=os.path.join(os.path.dirname(__file__),'static/upload/'+new_id)
        os.mkdir(upload_path)
        filename = upload_file['filename']
        newname = new_id+os.path.splitext(filename)[1]
        filepath = os.path.join(upload_path,newname)

        with open(filepath,'wb') as up:
            up.write(upload_file['body'])

        with Image(filename=filepath,resolution=90) as img:
            img.format="png"
            img.background_color = Color('white')
            img.save(filename=os.path.join(upload_path,'p.png'))
            coll = self.application.db.file
            newfile = {'filename':filename,'file_id':new_id,'width':img.width,'height':img.height}
            coll.insert(newfile)
        self.write(' <a href="/show/'+newname+'">查看</a> ')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
