import cherrypy
import os
import sqlite3
import httplib
import time
from Queue import Queue
from threading import Thread
import random

global queue
queue = Queue()


class Database(object):

    url_list = []

    def initialize_database(self):
        print 'I AM CONNECTING TO DB'
        self.connection = sqlite3.connect('sqlite3.db')

        while True:
            if queue.empty():
                time.sleep(0.5)
            print 'this is the get'
            queue.get()
            queue.task_done()

    def read_the_table(self):
        """Returns icon, url, last checked,
        ping status, ping ping_latency,
        and http status from database"""
        connection = self.connection.cursor()
        connection = connection.execute("SELECT * from sites")
        table = connection.fetchall()

        icon_list = []
        last_checked_list = []
        ping_status_list = []
        ping_latency_list = []
        http_status_list = []
        self.url_list = []

        for item in table:
            self.url_list.append(item[1])
            icon_list.append(item[2])
            ping_latency_list.append(item[3])
            ping_status_list.append(item[4])
            ping_latency_list.append(item[5])
            http_status_list.append(item[6])

        connection.close()
        # print "in this method, list is " + str(db.url_list)
        self.table_prep = {
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
        print url
        self.connection.execute(
            "INSERT INTO sites (site_url) VALUES (?)", (url,))
        time.sleep(100)

    def delete_a_site(self, url):
        """Delete site from database.

        Keyword arguments:
        delete_site -- the url of the site to be deleted
        """
        self.connection.execute("DELETE FROM sites WHERE Site_Url=?",
                                [url])

global db
db = Database()
worker = Thread(target=db.initialize_database)
worker.setDaemon(True)
worker.start()


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
        if len(db.url_list) == 0:
            time.sleep(1)
        print "For checking purposes: in site_status, list is" + str(db.url_list)
        result_list = []
        for url in db.url_list:
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

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def background_status_check(self):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def store_last_status(self):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def icon_upload(self):"""

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add_site(self, url):
        print 'this is url in add_site'
        print url
        # db.add_a_site(url)
        queue.put(db.add_a_site(url))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete_site(self, url):
        # db.delete_a_site(url)
        queue.put(db.delete_a_site(url))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def read_table(self):
        print 'READING THE TABLE'
        queue.put(db.read_the_table())
        time.sleep(1)
        while db.table_prep == None:
            time.sleep(0.1)
        print db.table_prep
        return db.table_prep


class App(object):
    """
    def __init__(self):
        print 'threading.enumerate  in App init is'
        print threading.enumerate()
        print 'threading.active count in App init is'
        print threading.active_count()     
        print 'threading.current in App init is'
        print threading.current_thread()
        """

    @cherrypy.expose
    def index(self):
        # db.initialize_database()
        return open("./public/Site Monitoring Dashboard.html",
                    'r').read()

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

app = App()
app.site = Site()
cherrypy.tree.mount(app, '/', conf)
cherrypy.tree.mount(app.site, '/Site')

cherrypy.engine.start()
cherrypy.engine.block()
