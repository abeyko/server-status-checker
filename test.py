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

    # This function fetches the 2 columns from the popular_sites
    # table in my.db and returns 2 lists
    # JS loops through each list and adds an identifier to each icon and url
    # in the popular sites list by referencing this function
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

    # This function fetches 1 column from the my_sites
    # table in my.db and returns one list
    # JS loops through each list and adds an identifier to each url in the my
    # sites list by referencing this function
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

    # Takes the values submitted via button press and adds it as a new row in
    # the my_sites table
    @cherrypy.expose
    def append_my_sites(self, newSite):
        with sqlite3.connect('my.db') as c:
            cherrypy.session['ts'] = time.time()
            c.execute("INSERT INTO my_sites VALUES (?, ?)",
                      [cherrypy.session.id, newSite])
            return newSite

    @cherrypy.expose
    def delete_site(self, the_url):
        cherrypy.session.pop('ts', None)
        with sqlite3.connect('my.db') as c:
            c.execute("DELETE FROM my_sites WHERE Site_Url=?",
                [the_url])
            #c.execute("DELETE FROM my_sites WHERE session_id=?",
                #[cherrypy.session.id])  

    # Pings each url in site_url list from popular_sites table and returns
    # checkmark or cross wingding depending if the site is up or down
    # I want it to include both tables now...
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_data(self):
        conn = sqlite3.connect('my.db')
        print "Connected to my db"
        c = conn.cursor()
        c.execute("SELECT site_url FROM popular_sites")
        res = c.fetchall()
        res = list(res)
        c.execute("SELECT Site_Url FROM my_sites")
        res2 = c.fetchall()
        res2 = list(res2)
        c.close()
        ser = []
        res_joined = res + res2
        for item in res_joined:
            ping_item = item[0]
            if ping_item.startswith('http://'):
                ping_item = ping_item[7:]
                print ping_item
            print type(item)
            print type(ping_item[0])
            ping_response = os.system("ping -c 1 -W 5 " + ping_item)
            # try out pythonic version of ping, something compatible for
            # windows users
            new_item = item[0]
            response = requests.get(new_item)
            # try to use httplib instead of requests, suppposed to be faster
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
