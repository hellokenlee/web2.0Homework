import tornado.ioloop
import tornado.web
import os
import os.path
import sys
path = os.path.abspath(os.path.dirname(sys.argv[0]))
rootdir=os.path.join(path,"static")
rootdir=os.path.join(rootdir,"songs")

settings = {
    "static_path": rootdir,
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
}

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		for parent,dirnames,filenames in os.walk(rootdir): 
				self.render("music.html",files=filenames)
				
application = tornado.web.Application(
    handlers=[(r'/', MainHandler)],
	static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
if __name__ == "__main__":
    application.listen(8887)
    tornado.ioloop.IOLoop.instance().start()