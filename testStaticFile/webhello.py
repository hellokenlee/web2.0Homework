import tornado.ioloop
import tornado.web
import os.path

class MainHandler( tornado.web.RequestHandler):
	def get(self):
		self.render("music.html")

		
application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/songs/(.*)",tornado.web.StaticFileHandler,{"path": "./songs"})
	], 
	debug=True)

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()