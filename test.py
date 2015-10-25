import cherrypy
import os
import simplejson
import MySQLdb
import requests


class AjaxApp(object):

    @cherrypy.expose
    def index(self):
        return open("./public/index.html",
                    'r').read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_data(self):
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
            ping_response = os.system("ping -c 1 -W 5 " + item[0])
            new_item = 'http://' + item[0]
            response = requests.get(new_item)
            http_response = response.status_code
            print response.status_code, response.url
            # how to handle error 503?
            if ping_response == 0 or http_response == 200:
                ser.append(u"\u2705")
            else:
                ser.append(u"\u274e")
        return {
            'res': ser
        }

    @cherrypy.expose
    def submit(self, name):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(title="Hello, %s" % name))

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

    cherrypy.quickstart(AjaxApp(), '/', conf)
