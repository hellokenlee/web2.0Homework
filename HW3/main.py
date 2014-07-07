import tornado.ioloop
import tornado.web
import os
import os.path
import sys
import string
movie="tmnt2"
rootdir=os.path.abspath('.')
filedir=os.path.join(rootdir,"static")
filedir=os.path.join(filedir,"moviefiles")
filedir=os.path.join(filedir,movie)

settings = {
    "static_path": os.path.join(rootdir,"static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
}

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		f=open(os.path.join(filedir,"info.txt"))
		info=f.read().splitlines()
		digit=string.atoi(info[2])
		g=open(os.path.join(filedir,"generaloverview.txt"))
		overview=g.read().splitlines()
		keys=[]
		vals=[]
		for ov in overview:
			tmp=ov.split(':')
			keys.append(tmp[0])
			vals.append(tmp[1])
		l=len(keys)
		filenames=os.listdir(filedir)
		reviews=[]
		for filename in filenames:
			if filename[0:6]=="review":
				f=open(os.path.join(filedir,filename))
				tmp=f.read().splitlines()
				reviews.append(tmp)
		
		self.render('main.html',rootdir=rootdir,movie=movie,info=info,keys=keys,vals=vals,l=l,reviews=reviews,digit=digit)

				
application = tornado.web.Application(
    handlers=[(r'/', MainHandler)],
	static_path=os.path.join(rootdir, "static"),
    )
	
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
