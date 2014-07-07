import web
urls = (
	'/','MainHandler',
	'/login','LoginHandler',
	'/loutout','LogoutHandler',
	'/(\w+)/Feeng/1','BlogHandler',
)

app = web.application(urls,globals())
class BaseHandler:
	def get_current_user(self):
		return web.cookies().get("user")

class MainHandler(BaseHandler):
	def GET(self):
		if not self.get_current_user:
			web.seeother("/login")
			return
		else:
			name = self.get_current_user
			slef.redirect("/"+name+"/Fenng/1")

class LoginHandler(BaseHandler):
	def  GET(self):
		self.write('<html><body><form action="/login" method="post">'
                   'User: <input type="text" name="name">'
				   'Password:<input type="password" name="psw">'
				   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

	def post(self):
		usr = 