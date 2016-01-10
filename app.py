import cherrypy
import os
import sqlite3
import httplib
import time
from threading import Thread
from urlparse import urlparse
import re
import subprocess
import urllib
import datetime

up_symbol = 9989
down_symbol = 10062

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

global background_worker
background_started = False

class Database(object):

    url_list = []

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def read_the_table(self):
        """Returns icon, url, last checked,
        ping status, ping ping_latency,
        and http status from database"""
        table = database_connection(0, "SELECT * from sites")

        icon_list = []
        db.url_list = []
        db.url_list2 = []
        last_checked_list = []
        status_icon_list = []
        ping_status_list = []
        ping_latency_list = []
        http_status_list = []

        for item in table:
            icon_list.append(item[1])
            db.url_list.append(item[2])
            last_checked_list.append(item[3])
            status_icon_list.append(unichr(item[4]))
            ping_status_list.append(item[5])
            ping_latency_list.append(item[6])
            http_status_list.append(item[7])
        print status_icon_list

        global background_started
        print "Background worker is starting"
        if not background_started:
            global background_worker
            background_worker = Thread(target=update)
            background_worker.setDaemon(True)
            background_worker.start()
            background_started = True

        for url in db.url_list:
            #strip url down here
            o = urlparse(url)
            domain = o.hostname
            temp = domain.rsplit('.')
            if (len(temp) == 3):
                domain = temp[1] + '.' + temp[2]
                print 'domain is ' + str(domain)

            db.url_list2.append(domain)


        return {
            'icon_list': icon_list,
            'url_list': db.url_list2,
            'last_checked_list': last_checked_list,
            'status_icon_list': status_icon_list,
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
        database_connection(
            1, "INSERT INTO sites (site_url) VALUES (\"" + url + "\")")

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
global url_list
url_list = db.url_list


class Site(object):

    def background_status_check(self):
        """Return an up or down status icon after
        checking each url in the database"""
        status_icon_list = []
        last_checked_list = []
        ping_response_list = []
        ping_latency_list = []
        http_status_list = []

        if len(db.url_list) == 0:
            time.sleep(1)
        print "For checking purposes: in background_status_check, list is" + str(db.url_list)
        
        for url in db.url_list:
            print 'url before ping_item is ' + url
            print 'type for url is ' + str(type(url))
            # result was unicode here
            if isinstance(url, unicode):
                ping_item = str(url)
                print 'if isinstance was unicode, ping item is now ' + str(ping_item)
            else:
                ping_item = str(url[0])
                print 'if isinstance was not unicode, ping item is now ' + str(ping_item)

            http_item = ping_item
            url_item = ping_item

            ping_item_parse = urlparse(ping_item)
            ping_item = ping_item_parse.hostname

            ping_response = 42
            ping_latency = 5000

            try:
                ping = subprocess.Popen(["ping", "-n", "-c 1", ping_item], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, error = ping.communicate()
                print 'ping is ' + str(ping)
                print 'out is ' + str(out) 
                if out:
                    try:
                        ping_latency = int(re.findall(r"time=(\d+)", out)[0])
                        ping_response = int(re.findall(r"(\d+) packets received", out)[0])
                        print 'packets recieved are ' + str(ping_response)
                        print "ping latency type = " + str(ping_latency)
                        print 'time is ' + str(time) + 'ms'
                    except:
                        print "error occurred finding time"
                        ping_response = 0
                        ping_latency = 'None'
                    else:
                        print 'No ping'
                        #this doens't make sense

            except subprocess.CalledProcessError:
                print "Couldn't get a ping"

            open_url = urllib.urlopen(http_item)
            final_url = open_url.geturl()
            http_code = open_url.getcode()
            print 'final url was ' + str(final_url)
            print 'http code is ' + str(http_code)

            #c_time = time.ctime()
            c_time = time.strftime("%x %X")

            #c_time = datetime.datetime.strptime(time.ctime(), "%x %X") 


            if ping_response == 1 \
                    or http_code >= 500 or \
                    http_code <= 399 or \
                    http_code == 405:
                global up_symbol
                global down_symbol
                status_icon = up_symbol
            else:
                status_icon = down_symbol

            last_checked_list.append(c_time)           
            ping_response_list.append(ping_response)
            ping_latency_list.append(ping_latency)
            http_status_list.append(http_code)
            executible = "UPDATE sites SET last_checked=  (\"" + str(c_time) + "\"), status_icon= (\"" + str(status_icon) + "\"), ping_status= (\"" + str(ping_response) + "\"), ping_latency= (\"" + str(ping_latency) + "\"), http_status= \"" + str(http_code) + "\" WHERE site_url = (\"" + url_item + "\") "
            print 'executible is ' + str(executible)
            database_connection(1, executible)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def single_status_check(self, url):
        single = "check single status here"

global s
s = Site()

def update():
    while True:
        print "update function is running"
        s.background_status_check()
        time.sleep(100)

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