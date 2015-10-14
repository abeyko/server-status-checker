import cherrypy
import os

class App():
	@cherrypy.expose
	def index(self):
		return open("/Users/Angeliki/Desktop/icon_test/public/index.html",'r').read()

	def addSite(self,name=None):
		if name:
			output="Hello %s !" % name
		else:
			output="You must enter a website!"
		return output
	addSite.exposed = True

if __name__ == '__main__':
	conf = {
	'/': {
		 'tools.sessions.on': True,
		 'tools.staticdir.root': os.path.abspath(os.getcwd())
	 },
	 '/static': {
		 'tools.staticdir.on': True,
		 'tools.staticdir.dir': './public'
	 }
	}
	
cherrypy.quickstart(App(), '/', conf)