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
		res = list()
		global db
		db=MySQLdb.connect(host="localhost", user="root", passwd="password", db="popular_sites")
		c = db.cursor()
		c.execute('SELECT site_url FROM popular_sites')
		res = c.fetchall()
		res = list(res)
		c.close()
		ser = []
		for item in res:

			response = os.system("ping -c 1 " + item[0])
			
			if response == 0:
				ser.append("is up! :D")				
			else:
				ser.append("is down! :'(")				

		return {
			'res' : ser
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