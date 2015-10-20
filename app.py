import cherrypy
import os
import MySQLdb
import urllib
import httplib
import urllib2
import requests


class Root():

    @cherrypy.expose
    def index(self):
        return open("/Users/Angeliki/Desktop/icon_test/public/index.html",
                    'r').read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getData(self):
        res = list()
        global db
        db = MySQLdb.connect(
            host="localhost", user="root",
            passwd="password", db="popular_sites")
        c = db.cursor()
        c.execute('SELECT site_url FROM popular_sites')
        res = c.fetchall()
        res = list(res)
        c.close()
        ser = []
        for item in res:

            ping_response = os.system("ping -c 1 -W 5 " + item[0]) #should set a timeout for ping
            
            newitem = 'http://' + item[0] # method 3 works!
            response = requests.get(newitem) # method 3 works!
            response.history #(<Response [302]>, <Response[302]>, <Response [302]>) # method 3 works!
            #for resp in response.history: # method 3 works!
            	#print resp.status_code, resp.url # method 3 works!
            #print response.status_code, response.url # method 3 works!
            #print response.status_code # method 3 works!
            http_response = response.status_code

 
            if ping_response == 0 or http_response == 200:
            	ser.append("is up! :D")
            else:
                ser.append("is down! :'(")

        return {
            'res': ser
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
