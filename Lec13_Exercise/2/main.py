# -*- coding: utf-8 -*-
#by KENLEE
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import os
import os.path
import sys
import string
import json
class blog:
	def __init__(self,title,detail,content):
		self.title=title
		self.detail=detail
		self.content=content

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/comment", CommentHandler),
			(r"/", MainHandler)
		]
		conn = pymongo.Connection("localhost", 27017)         #实例化一个pymongo连接对象
		self.db = conn["paperDB"]			                  #在Application对象中创建一个db属性连接到paperDB数据库
		settings = dict(
			static_path=os.path.join(os.path.dirname(__file__),'static'),#静态路径
			template_path=os.path.join(os.path.dirname(__file__), 'templates'),#模板路径
			debug=True
		)
		tornado.web.Application.__init__(self, handlers, **settings)
		
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		info=self.application.db.infoDB
		for one in info.find():
			all=one
		b=blog(all["title"],all["detail"],all["content"])
		commentlist=all["comment"]
		jsons=[]
		for comment in commentlist:
			jsons.append(comment)
		print jsons
		self.render("blog.html",blog=b)

class CommentHandler(tornado.web.RequestHandler):
	def get(self):
		print "Comment calling\n"
		info=self.application.db.infoDB
		for one in info.find():
			all=one
		commentlist=all["comment"]
		jsonlist=[]
		for comment in commentlist:#转成JSON格式
			jsonlist.append(comment)
		if self.get_argument("jsoncallback"):
			resp_string = self.get_argument("jsoncallback") +"("+ json.dumps(jsonlist)+")"
		else:
			resp_string = json.dumps(jsonlist)
		self.write(resp_string)
		
if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()