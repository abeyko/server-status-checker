import cherrypy
import os
import simplejson
import sqlite3
import requests
import time


class AjaxApp(object):

    @cherrypy.expose
    def index(self):
        return open("./public/index.html",
                    'r').read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_tables(self):
        conn = sqlite3.connect('my.db')
        c = conn.cursor()
        c.execute("SELECT site_url FROM popular_sites")
        res = c.fetchall()
        res = list(res)
        c.execute("SELECT icon_url FROM popular_sites")
        res2 = c.fetchall()
        res2 = list(res2)
        print "res is a type "
        print type(res)
        c.close()
        return {
            'site_url': res,
            'icon_url': res2
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_other_table(self):
        conn = sqlite3.connect('my.db')
        c = conn.cursor()
        c.execute("SELECT site_url FROM my_sites")
        res3 = c.fetchall()
        res3 = list(res3)
        print "res is a type "
        print type(res3)
        c.close()
        return {
            'site_url': res3
        }

    @cherrypy.expose
    def append_my_sites(self, newSite):
        with sqlite3.connect('my.db') as c:
            cherrypy.session['ts'] = time.time()
            c.execute("INSERT INTO my_sites VALUES (?, ?)",
                      [cherrypy.session.id, newSite])
            return newSite

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_data(self):
        conn = sqlite3.connect('my.db')
        c = conn.cursor()
        c.execute("SELECT site_url FROM popular_sites")
        res = c.fetchall()
        res = list(res)
        print "res is a type "
        print type(res)
        c.close()
        ser = []
        for item in res:
            ping_item = item[0]
            if ping_item.startswith('http://'):
                ping_item = ping_item[7:]
                print ping_item
            print type(item)
            print type(ping_item[0])
            ping_response = os.system("ping -c 1 -W 5 " + ping_item)
            new_item = item[0]
            response = requests.get(new_item)
            http_response = response.status_code
            print response.status_code, response.url
            if ping_response == 0 or http_response == 200:
                ser.append(u"\u2705")
            else:
                ser.append(u"\u274e")
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

cherrypy.quickstart(AjaxApp(), '/', conf)
