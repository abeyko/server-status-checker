import atexit
import threading
import cherrypy 
import os
import MySQLdb 

class Root():
	@cherrypy.expose
	def index(self):
		return open("/Users/Angeliki/Desktop/icon_test/public/index.html",'r').read()
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def getData(self):
		global db
		db=MySQLdb.connect(host="localhost", user="root", passwd="password", db="popular_sites")
		c = db.cursor()
		c.execute('SELECT count(*) FROM popular_sites')
		res = c.fetchall()
		res = ','.join(str(r) for r in res)
		c.close
		return {
			'res' : res
		}
	

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
	
cherrypy.quickstart(Root(), '/', conf)