import cherrypy
import os
import sqlite3
import httplib
import time

def database_connection(decider, command):
    connection = sqlite3.connect('sqlite3.db')
    if decider == 0:
        connection = connection.cursor()
        connection.execute(command)
        fetch = connection.fetchall()
        connection.close()
        return fetch
    if decider == 1:
        print command
        connection.execute(command)
        connection.commit()
        connection.close()
        return "ran"


class Database(object):

    url_list = []

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def read_the_table(self):
        """Returns icon, url, last checked,
        ping status, ping ping_latency,
        and http status from database"""
        table = database_connection(0, "SELECT * from sites")

        icon_lista = []
        last_checked_list = []
        ping_status_list = []
        ping_latency_list = []
        http_status_list = []
        db.url_list = []

        for item in table:
            db.url_list.append(item[1])
            icon_lista.append(item[2])
            ping_latency_list.append(item[3])
            ping_status_list.append(item[4])
            ping_latency_list.append(item[5])
            http_status_list.append(item[6])

        return {
            'icon_list': icon_lista,
            'url_list': db.url_list,
            'last_checked_list': last_checked_list,
            'ping_status_list': ping_status_list,
            'ping_latency_list': ping_latency_list,
            'http_status_list': http_status_list
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add_a_site(self, url):
        """Add site to database.

        Keyword arguments:
        add_site -- the url of the site to be added
        """
        url = str(url)
        print 'the url that was added is'
        command_output = database_connection(
            1, "INSERT INTO sites (site_url) VALUES (\"" + url + "\")")
        print command_output

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete_a_site(self, url):
        """Delete site from database.

        Keyword arguments:
        delete_site -- the url of the site to be deleted
        """
        database_connection(
            1, "DELETE FROM sites WHERE Site_Url= \"" + url + "\"")

global db
db = Database()

class Site(object):
    url_list = db.url_list
    print 'in site class url list is'
    print url_list

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
            # print "------------------START-------------------"
            # print "LEVEL: " + str(depth)
            # print "URL: " + url
            url = url[7:]
            if url.endswith('/'):
                url = url[:-1]
            url = str(url)
            # print "URL STRIPPED: " + url
            connection = httplib.HTTPConnection(url)

        if url.startswith('https://'):
            # print "LEVEL: " + str(depth)
            # print "URL: " + url
            url = url[8:]
            url = url[:-1]
            url = str(url)
            # print "URL STRIPPED: " + url
            connection = httplib.HTTPSConnection(url)

        #print "url is " + str(url)
        request = connection.request("HEAD", "/", body, headers)
        response = connection.getresponse()
        # print "STATUS: " + str(response.status)
        # print "REASON: " + str(response.reason)

        headers = dict(response.getheaders())
        if 'location' in headers and headers['location'] != url:
            # print "NEW LOCATION: " + headers['location']
            if 'location' in headers and headers['location'] == '/':
                return "will not pursue"
            # print "-----------------------------------------"
            return self.httpredirect(headers['location'], depth + 1)
        else:
            final_status = response.status
            # print "-----------------FINISH-------------------"
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
            # print 'THIS IS URL'
            # print url
            if ping_item.startswith('http://'):
                ping_item = ping_item[7:]
            ping_response = os.system("ping -c 1 -W 1 " + ping_item)
            http_status = self.httpredirect(http_item, 0)
            if ping_response == 0 \
                    or http_status >= 500 or \
                    http_status <= 399 or \
                    http_status == 405:
                # print http_status
                # print ping_response
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


class App(object):

    @cherrypy.expose
    def index(self):
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
app.site.database = Database()
cherrypy.tree.mount(app, '/', conf)
cherrypy.tree.mount(app.site, '/Site')
cherrypy.tree.mount(app.site.database, '/Site/Database')

cherrypy.engine.start()
cherrypy.engine.block()
