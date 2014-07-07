# -*- coding: utf-8 -*-
#by KENLEE
import pymongo
import os
import os.path
import sys
import string
import json
import tornado.ioloop
import tornado.web
import time
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
		db=conn["test2"]
		user=db.users
		data=user.find_one({"usr":author_name})
		if data==None:
			self.redirect("http://thebest404pageever.com/")
			self.set_status(404)
			return		
		f=open("data/blog.txt")
		all=f.read().splitlines()
		title=((all[0]).split(':'))[1]
		author=((all[1]).split(':'))[1]
		content=((all[2]).split(':'))[1]
		
		comments=db.comments
		coms=[]
		for all_com in comments.find():
			coms.append([all_com["name"],all_com["time"],all_com["content"]])
		name = tornado.escape.xhtml_escape(self.current_user)
		self.render('blog.html',title=title,author=author,content=content,coms=coms,a_name=author_name,name=name)
		
	def post(self,author_name):
		o=open("data/comments.txt","a")
		name = author_name
		t=time.strftime('%Y-%m-%d',time.localtime(time.time()))
		comm=self.get_argument("com")
		output=name+"|"+t+"|"+comm+"\n"
		print output
		o.write(output)
		self.redirect("/"+author_name+"/Fenng/1")
		
class CommentHandler(BaseHandler):
	def get(self,usr_name):
		conn = pymongo.Connection("localhost", 27017)         #实例化一个pymongo连接对象
		db=conn["test2"]
		comments=db.comments
		content=self.get_argument("text")
		t=time.strftime('%Y-%m-%d',time.localtime(time.time()))
		comments.insert({"name":usr_name,"time":t,"content":content})
		jsonlist=[]
		jsonlist.append(usr_name)
		jsonlist.append(t)
		jsonlist.append(content)
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
		db=conn["test2"]
		user=db.users
		data=user.find_one({"usr":usr})
		if data==None:
			self.redirect("/login")
			return
		else:
			pw=data["psw"]
			if pw!=psw:
				self.redirect("/login")
				return
			else:
				self.set_secure_cookie("user",usr)
				self.redirect("/"+usr+"/Fenng/1")
				return

class RegisterHandler(BaseHandler):
	def get(self):
		self.render("register.html")

	def post(self):
		usr = self.get_argument("name")
		psw1 = self.get_argument("psw1")
		psw2 = self.get_argument("psw2")
		if psw1!=psw2:
			self.redirect("/register")
			return
		else:
			conn = pymongo.Connection("localhost", 27017)         #实例化一个pymongo连接对象
			db=conn["test2"]
			user=db.users
			user.insert({"usr":usr,"psw":psw1})
			self.redirect("/login")
			return
		
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
	(r"/logout", LogoutHandler),
	(r"/(\w+)/Fenng/1",BlogHandler),
	(r"/register",RegisterHandler),
	(r"/(\w+)/Fenng/1/comment",CommentHandler)
], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=" ,debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()