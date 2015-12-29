import cherrypy
import os
import sqlite3
import httplib
import time
import threading
import random

# icon | url | last checked | status icon | ping status | ping_latency | http_status code | weekly stats | delete | ping now 


class Database(object):

    url_list = []
    """
    def __init__(self):
        
        print 'I AM CONNECTING TO DB'
        self.connection = sqlite3.connect('sqlite3.db')
        print 'threading.enumerate  in Database init is'
        print threading.enumerate()
        print 'threading.active count in Database init is'
        print threading.active_count()
        print 'threading.current in Database init is'
        print threading.current_thread()
    """
    def initialize_database(self):
        print 'I AM CONNECTING TO DB'
        self.connection = sqlite3.connect('sqlite3.db')
        print 'threading.enumerate  in Database init is'
        print threading.enumerate()
        print 'threading.active count in Database init is'
        print threading.active_count()
        print 'threading.current in Database init is'
        print threading.current_thread()

    def read_the_table(self):
        """Returns icon, url, last checked,
        ping status, ping ping_latency,
        and http status from database"""
        print 'threading.enumerate in Database read_the_table is'
        print threading.enumerate()
        print 'threading.active count in Database read_the_table is'
        print threading.active_count()
        print 'threading.current in Database read_the_table is'
        print threading.current_thread()  
        print 'HEY, THESE ARE THE KEYS'
        print cherrypy.tree.apps.keys()
        #connection = sqlite3.connect('sqlite3.db')
        connection = self.connection.cursor()
        connection = connection.execute("SELECT * from sites")
        table = connection.fetchall()
        print 'This is table'
        print table

        #global url_list
        #url_list = []
        icon_list = []
        last_checked_list = []
        ping_status_list = []
        ping_latency_list = []
        http_status_list = []

        for item in table:
            self.url_list.append(item[1])
            icon_list.append(item[2])
            ping_latency_list.append(item[3])
            ping_status_list.append(item[4])
            ping_latency_list.append(item[5])
            http_status_list.append(item[6])

        connection.close()
        print "in this method, list is " + str(db.url_list)
        return {
            'icon_list': icon_list,
            'url_list': db.url_list,
            'last_checked_list': last_checked_list,
            'ping_status_list': ping_status_list,
            'ping_latency_list': ping_latency_list,
            'http_status_list': http_status_list
        }

    def add_a_site(self, url):
        """Add site to database.

        Keyword arguments:
        add_site -- the url of the site to be added
        """
        connection.execute("INSERT INTO sites(site_url) VALUES (?)",
                           [url])

    def delete_a_site(self, url):
        """Delete site from database.

        Keyword arguments:
        delete_site -- the url of the site to be deleted
        """
        connection.execute("DELETE FROM sites WHERE Site_Url=?",
                               [url])

global db
db = Database()

class Site(object):
    url_list = db.url_list
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def httpredirect(self, url, depth=0):
        """Handles http redirects. Returns final http status.

        Keyword arguments:
        url -- the url of the site to request http or https status
        depth -- the number of times a redirect occured (default 0)
        """
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
            connection = httplib.HTTPConnection(url)

        if url.startswith('https://'):
            print "LEVEL: " + str(depth)
            print "URL: " + url
            url = url[8:]
            url = url[:-1]
            url = str(url)
            print "URL STRIPPED: " + url
            connection = httplib.HTTPSConnection(url)

        print "url is " + str(url)
        request = connection.request("HEAD", "/", body, headers)
        response = connection.getresponse()
        print "STATUS: " + str(response.status)
        print "REASON: " + str(response.reason)

        headers = dict(response.getheaders())
        if 'location' in headers and headers['location'] != url:
            print "NEW LOCATION: " + headers['location']
            if 'location' in headers and headers['location'] == '/':
                return "will not pursue"
            print "-----------------------------------------"
            return self.httpredirect(headers['location'], depth + 1)
        else:
            final_status = response.status
            print "-----------------FINISH-------------------"
            print " "
            return final_status

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def site_status(self):
        """Return an up or down status icon after
        checking each url in the database"""
        time.sleep(10)
        print "For checking purposes: in site_status, list is" + str(db.url_list)
        result_list = []
        for url in self.url_list:
            ping_item = url
            http_item = url
            print 'THIS IS URL'
            print url
            if ping_item.startswith('http://'):
                ping_item = ping_item[7:]
            ping_response = os.system("ping -c 1 -W 1 " + ping_item)
            http_status = self.httpredirect(http_item, 0)
            if ping_response == 0 \
                    or http_status >= 500 or \
                    http_status <= 399 or \
                    http_status == 405:
                print http_status
                print ping_response
                result_list.append(u"\u2705")
            else:
                result_list.append(u"\u274e")
        return {
            'result': result_list
        }

    """@cherrypy.expose
    @cherrypy.tools.json_out()
    def single_status_check(self):
        hi = "hi"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def background_status_check(self):
        hi = "hi"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def store_last_status(self):
        hi = "hi"

    @cherrypy.expose
    # does cherrpy.expose mean it needs its own thread?
    @cherrypy.tools.json_out()
    def icon_upload(self):
        hi = "hi"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add__site(self):
        db.add_a_site(url)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete_site(self):
        db.delete_a_site(url)"""

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def read_table(self):
        print 'DOING THE THING'
        return db.read_the_table()

class App(object):

    def __init__(self):
        print 'threading.enumerate  in App init is'
        print threading.enumerate()
        print 'threading.active count in App init is'
        print threading.active_count()     
        print 'threading.current in App init is'
        print threading.current_thread()    

    @cherrypy.expose
    def index(self):
        db.initialize_database()
        print 'threading.enumerate  in App index is'
        print threading.enumerate()
        print 'threading.active count in App index is'
        print threading.active_count()
        print 'threading.current in App index is'
        print threading.current_thread()  
        return open("./public/Site Monitoring Dashboard.html",
                    'r').read()

    
def reverse(cls):
    #return cherrypy.tree.apps.keys()
    #return dir(cherrypy.tree.apps[''].root)
    #return dir(cherrypy.tree.apps['/page3/apple'].root)
    # get link to apple
    for app_url in cherrypy.tree.apps.keys():
        if isinstance(cherrypy.tree.apps[app_url].root, cls):
            # NOTE: it will return with the first instance
            return app_url

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

#cherrypy.app = App()
#cherrypy.app.site = Site()
#cherrypy.app.site.database = Database()

app = App()
app.site = Site()
#app.site.database = db
cherrypy.tree.mount(app, '/', conf)
cherrypy.tree.mount(app.site, '/Site')
#cherrypy.tree.mount(app.site.database, '/Database')

print 'This is link to site'
link_to_site = reverse(Site)
cherrypy.engine.start()
cherrypy.engine.block()
