# -*- coding: UTF-8 –*-
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
			(r"/service",MainHandler),
		]
		settings=dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			debug=True
			)
		self.obj=[
		   {
			"name":"britneyspears",
			"age":32,
			"email":"britneyspears@xxx.com"
		   },
		   {
			"name":"greenday",
    		"age":26,
    		"email":"greenday@xxx.com",
		   },
		   {
			"name":"U2",
    		"age":37,
    		"email":"U2@xxx.com",
		   }
		]
		tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		name=self.get_argument("name")
		imfo=None;
		for ob in self.application.obj:
			if ob["name"]==name:
				imfo=ob;
		if imfo==None:
			self.write('<html><body>Not Found!</body></html>');
		else:
			self.write(imfo);
if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
