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
		f=open("data/users.txt")
		users=f.read().splitlines()
		str1 = users[0].split(',')
		str2 = users[1].split(',')
		if author_name!=str2[0] and author_name!=str1[0]:
			self.redirect("http://thebest404pageever.com/")
			self.set_status(404)
			return
				
		f=open("data/blog.txt")
		all=f.read().splitlines()
		title=((all[0]).split(':'))[1]
		author=((all[1]).split(':'))[1]
		content=((all[2]).split(':'))[1]
		c=open("data/comments.txt")
		coms=[]
		all_coms=c.read().splitlines()
		for all_com in all_coms:
			coms.append(all_com.split('|'))
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
		
class LogoutHandler(BaseHandler):
	def get(self):
		self.set_secure_cookie("user", "")
		self.redirect("/")
		
		
		
class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'User: <input type="text" name="name">'
				   'Password:<input type="password" name="psw">'
				   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
		usr = self.get_argument("name")
		psw = self.get_argument("psw")
		f=open("data/users.txt")
		users=f.read().splitlines()
		for user in users:
			str= user.split(',')
			if usr==str[0] and psw==str[1]:
				self.set_secure_cookie("user",self.get_argument("name"))
				self.redirect("/"+usr+"/Fenng/1")
				return
		self.redirect("/login")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
	(r"/logout", LogoutHandler),
	(r"/(\w+)/Fenng/1",BlogHandler),
], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=" ,debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()