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

num_dict={'1':'Jan','2':'Feb','3':'Mar','4':'Apl','5':'May','6':'Jun','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}
month_dict={'Jan':1,'Feb':2,'Mar':3,'Apl':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
def cmpDate(a_dict,b_dict):
	a=a_dict["time"]
	b=b_dict["time"]
	a_datas=a.split(" ")
	b_datas=b.split(" ")
	if a_datas[2]!=b_datas[2]:
		return cmp(string.atoi(a_datas[2]),string.atoi(b_datas[2]))
	elif a_datas[0]!=b_datas[0]:
		return cmp(month_dict[a_datas[0]],month_dict[b_datas[0]])
	elif a_datas[1]!=b_datas[1]:
		return cmp(string.atoi(a_datas[1]),string.atoi(b_datas[1]))
	else:
		a_time=a_datas[3].split(":")
		b_time=b_datas[3].split(":")
		if a_time[0]!=b_time[0]:
			return cmp(string.atoi(a_time[0]),string.atoi(b_time[0]))
		elif a_time[1]!=b_time[1]:
			return cmp(string.atoi(a_time[1]),string.atoi(b_time[1]))
		else:
			return cmp(string.atoi(a_time[2]),string.atoi(b_time[2]))


from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/login", LoginHandler),
			(r"/logout", LogoutHandler),
			(r"/twitter/(\w+)",BlogHandler),
			(r"/twitter/(\w+)/tweet",TwitterHandler),
			(r"/twitter/(\w+)/comment",CommnetHandler),
			(r"/twitter/(\w+)/commentsubmmit",CommentSubmmitHandler)
		]
		conn = pymongo.Connection("localhost", 27017)         #实例化一个pymongo连接对象
		self.db=conn["twitterDB"]
		settings = dict(
			static_path=os.path.join(os.path.dirname(__file__),'static'),#静态路径
			debug=True,
			cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class CommentSubmmitHandler(BaseHandler):
	def get(self,username):
		user=self.application.db.userSets
		tw=self.get_argument('content')
		text=self.get_argument("text")
		author=self.get_argument("author")
		data=user.find_one({"name":author})
		jsonlist=[]
		t=time.strftime('%b %d %Y %H:%M:%S',time.localtime(time.time()))
		for tweet in data["twitters"]:
			if tweet["content"]==tw:
				print "!!!!!!!!!!!!!!!!!!:",tweet["comments"]
				tweet["comments"].append({"comment_date": t,"comment_by": username,"comment_content": text})
				jsonlist.append(t)
				user.save(data)
		if self.get_argument("jsoncallback"):
			resp_string=self.get_argument("jsoncallback")+"("+json.dumps(t)+")"
		else:
			resp_string=json.dumps(jsonlist)
		self.write(resp_string)

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        else:
			name = tornado.escape.xhtml_escape(self.current_user)
			self.redirect("/twitter/"+name)
        

class BlogHandler(BaseHandler):
	def get(self,author_name):
		user=self.application.db.userSets
		data=user.find_one({"name":author_name})
		img_url=data["image"]
		age=str(data["age"])
		email=data["email"]
		friends=data["friends"]
		allTweets=[]
		for friend in friends:
			friendData=user.find_one({"name":friend})
			for fTweet in friendData["twitters"]:
				fTweet["name"]=friend
				allTweets.append(fTweet)
		for tweet in data["twitters"]:
			tweet["name"]=author_name;
			allTweets.append(tweet)
		allTweets.sort(cmpDate)
		self.render('blog.html',img_url=img_url,name=author_name,email=email,age=age,twitters=allTweets)

class CommnetHandler(BaseHandler):
	def get(self,username):
		user=self.application.db.userSets
		author=self.get_argument("author")
		data=user.find_one({"name":author})
		content=self.get_argument('text')
		jsonlist=[]
		for tweet in data["twitters"]:
			if tweet["content"]==content:
				if tweet.get("comments","notfound")!="notfound":
					for com in tweet["comments"]:
						print com
						jsonlist.append(com)
		if self.get_argument("jsoncallback"):
			resp_string=self.get_argument("jsoncallback")+"("+json.dumps(jsonlist)+")"
		else:
			resp_string=json.dumps(jsonlist)
		self.write(resp_string)
		
class TwitterHandler(BaseHandler):
	def get(self,usr_name):
		print "!!!!!!!!!!!!!!!!!!"
		user=self.application.db.userSets
		data=user.find_one({"name":usr_name})
		content=self.get_argument("text")
		print content
		t=time.strftime('%b %d %Y %H:%M:%S',time.localtime(time.time()))
		print data["twitters"]
		data["twitters"].append({"time":t,"content":content})
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
		user=self.application.db.userSets
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