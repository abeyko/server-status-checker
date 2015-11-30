import cherrypy
import os
import sqlite3
import httplib
import time


class App(object):

    @cherrypy.expose
    def index(self):
        return open("./public/index.html",
                    'r').read()

    # This function fetches the 2 columns from the popular_sites
    # table in my.db and returns 2 lists (site_url and icon_url)
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_table(self):
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
    # table in my.db and returns one list (site_url)
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_other_table(self):
        conn = sqlite3.connect('my.db')
        c = conn.cursor()
        c.execute("SELECT site_url FROM my_sites")
        res3 = c.fetchall()
        res3 = list(res3)
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

    # 'the_url' is found in the JS function 'delete_the_string'
    # which accepts a parameter 'e'. The function is called in
    # the html generation for 'my_sites' with siteUrl[i] as the
    # argument. Thus, each url has its associated 'Delete' button.
    # Here, it accesses the 'my_sites' table in 'my.db' and deletes
    # every record where 'Site_Url' = 'the_url' that was associated
    # with the 'Delete' button press
    @cherrypy.expose
    def delete_site(self, the_url):
        with sqlite3.connect('my.db') as c:
            c.execute("DELETE FROM my_sites WHERE Site_Url=?",
                      [the_url])

    @cherrypy.expose
    def resolve_httpredirect(self, url, depth=0):
        headers = {"User-Agent": "firefox"}
        body = ""
        if depth > 10:
            raise Exception("Redirected " + depth + "times, giving up.")
        if url.startswith('http://'):
            print "------------------START-------------------"
            print "LEVEL: " + str(depth)
            print "URL: " + url
            url = url[7:]
            if url.endswith('/'):
                url = url[:-1]
            url = str(url)
            print "URL STRIPPED: " + url
            conn = httplib.HTTPConnection(url)

        if url.startswith('https://'):
            print "LEVEL: " + str(depth)
            print "URL: " + url
            url = url[8:]
            url = url[:-1]
            url = str(url)
            print "URL STRIPPED: " + url
            conn = httplib.HTTPSConnection(url)

        print "url is " + str(url)
        req = conn.request("HEAD", "/", body, headers)
        res = conn.getresponse()
        print "STATUS: " + str(res.status)
        print "REASON: " + str(res.reason)

        headers = dict(res.getheaders())
        if 'location' in headers and headers['location'] != url:
            print "NEW LOCATION: " + headers['location']
            if 'location' in headers and headers['location'] == '/':
                return "will not pursue"
            print "-----------------------------------------"
            return self.resolve_httpredirect(headers['location'], depth + 1)
        else:
            final_status = res.status
            print "-----------------FINISH-------------------"
            print " "
            return final_status

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
            http_item = item[0]
            if ping_item.startswith('http://'):
                ping_item = ping_item[7:]
                print ping_item
            print type(item)
            print type(ping_item[0])
            ping_response = os.system("ping -c 1 -W 1 " + ping_item)
            # try multi-threading
            # try out pythonic version of ping, something compatible for
            # windows users
            print type(ping_item)
            print ping_item
            test_url = http_item
            stat = self.resolve_httpredirect(test_url, 0)
            print stat
            print ping_response
            # anything in 400's is a client side error
            # amazon neither status check works, how to circumnavigate error
            # 405?
            if ping_response == 0 or stat >= 500 or stat <= 399 or stat == 405:
                print stat
                print ping_response
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

cherrypy.quickstart(App(), '/', conf)
