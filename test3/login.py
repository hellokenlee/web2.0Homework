# -*- coding: utf-8 -*-
#by KENLEE
import tornado.httpserver
import pymongo
import os
import os.path
import sys
import string
import json
import tornado.ioloop
import tornado.web
import time

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/login", LoginHandler),
			(r"/logout", LogoutHandler),
			(r"/twitter/(\w+)",BlogHandler),
			(r"/twitter/(\w+)/comment",CommentHandler)
		]
		settings = dict(
			static_path=os.path.join(os.path.dirname(__file__),'static'),#静态路径
			debug=True,
			cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        else:
			name = tornado.escape.xhtml_escape(self.current_user)
			self.redirect("/"+name+"/Fenng/1")
        

class BlogHandler(BaseHandler):
	def get(self,author_name):
		conn = pymongo.Connection("localhost", 27017)         #实例化一个pymongo连接对象
		db=conn["twitterDB"]
		user=db.userSets
		data=user.find_one({"name":author_name})
		twitters=data["tweets"]
		img_url=data["image"]
		age=str(data["age"])
		email=data["email"]
		self.render('blog.html',img_url=img_url,name=author_name,email=email,age=age,twitters=twitters)

		
class CommentHandler(BaseHandler):
	def get(self,usr_name):
		conn = pymongo.Connection("localhost", 27017)         #实例化一个pymongo连接对象
		db=conn["twitterDB"]
		user=db.userSets
		data=user.find_one({"name":usr_name})
		content=self.get_argument("text")
		print content
		t=time.strftime('%Y-%m-%d',time.localtime(time.time()))
		print data["tweets"]
		data["tweets"].append({"time":t,"content":content})
		user.save(data)
		jsonlist=[]
		jsonlist.append(content)
		jsonlist.append(t)
		if self.get_argument("jsoncallback"):
			resp_string = self.get_argument("jsoncallback") +"("+ json.dumps(jsonlist)+")"
		else:
			resp_string = json.dumps(jsonlist)
		self.write(resp_string)
		
class LogoutHandler(BaseHandler):
	def get(self):
		self.set_secure_cookie("user", "")
		self.redirect("/")
		
		
		
class LoginHandler(BaseHandler):
    def get(self):
        self.render("index.html")

    def post(self):
		usr = self.get_argument("name")
		psw = self.get_argument("psw")
		conn = pymongo.Connection("localhost", 27017)         #实例化一个pymongo连接对象
		db=conn["twitterDB"]
		user=db.userSets
		data=user.find_one({"name":usr})
		print data
		if data==None:
			self.redirect("/login")
			return
		else:
			pw=str(data["password"])
			if pw!=psw:
				self.redirect("/login")
				return
			else:
				print("a!")
				self.set_secure_cookie("user",usr)
				self.redirect("/twitter/"+usr)
				return

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()