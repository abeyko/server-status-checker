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
import PIL
from PIL import Image
import logging
import sys


for arg in sys.argv:
    loglevel = str(arg)
    if loglevel.startswith('--log='):
        loglevel = loglevel[6:]
        print 'numeric_level is ' + str(loglevel)
        loglevel = loglevel.upper()
        print 'new numeric level is ' + str(loglevel)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=loglevel)


localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)


def database_connection(method, command):
    """Connects to database and selects or
    updates data.

    Keyword arguments:
    method -- database method
    command -- database command
    """
    logging.info('database_connection: Started')
    connection = sqlite3.connect('sqlite3.db')
    if method == 'select_data':
        connection = connection.cursor()
        logging.info('command is %s', command)
        connection.execute(command)
        fetched_data = connection.fetchall()
        connection.close()
        logging.info('database_connection: Finished Selecting Data')
        return fetched_data
    if method == 'update_data':
        logging.info('command is %s', command)
        connection.execute(command)
        connection.commit()
        connection.close()
        logging.info('database_connection: Finished Updating Data')


class Database(object):

    original_url_list = []

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def read_the_table(self):
        """Returns sites' icon, url, last
        checked, ping status, ping latency,
        and http status from database"""
        logging.info('Database:read_the_table: Started')
        table = database_connection('select_data', "SELECT * from sites")
        icon_list = []
        database.display_url_list = []
        database.original_url_list = []
        last_checked_list = []
        status_icon_list = []
        ping_status_list = []
        ping_latency_list = []
        http_status_list = []
        logging.info('table is %s', table)
        for row in table:
            icon_list.append(row[1])
            database.original_url_list.append(row[2])
            last_checked_list.append(row[3])
            if row[4] != None:
                status_icon_list.append(unichr(row[4]))
            else:
                status_icon_list.append(unichr(0))
            ping_status_list.append(row[5])
            ping_latency_list.append(row[6])
            http_status_list.append(row[7])
        for url in database.original_url_list:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            path = parsed_url.path
            domain = hostname + path
            if domain.startswith('www.'):
                domain = domain[4:]
            database.display_url_list.append(domain)
        logging.info('display url list is %s', database.display_url_list)
        logging.info('Database:read_the_table: Finished')
        return {
            'icon_list': icon_list,
            'display_url_list': database.display_url_list,
            'original_url_list': database.original_url_list,
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
        url -- the url of the site to be added
        """
        logging.info('Database:add_a_site: Started')
        logging.info('The url that is being added is %s', url)
        database_connection(
            'update_data',
            "INSERT INTO sites (site_url) VALUES (\"" + url + "\")")
        logging.info('Database:add_a_site: Finished')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete_a_site(self, url):
        """Delete site from database.

        Keyword arguments:
        url -- the url of the site to be deleted
        """
        logging.info('Database:delete_a_site: Started')
        logging.info('The url that is being deleted is %s', url)
        database_connection(
            'update_data', "DELETE FROM sites WHERE Site_Url= \"" + url + "\"")
        logging.info('Database:delete_a_site: Finished')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload_icon(self, myFile, url):
        """Upload image icon url in database.

        Keyword arguments:
        myFile -- the uploaded file
        url -- the url whose image icon is being added to database
        """
        logging.info('Database:upload_icon: Started')
        url_item_parse = urlparse(url)
        url_item_hostname = url_item_parse.hostname
        url_item_path = url_item_parse.path
        full_url = url_item_hostname + url_item_path
        size = 0
        newDir = absDir + "public/icons/"
        img = Image.open(myFile.file)
        img = img.resize((64, 64), PIL.Image.ANTIALIAS)
        file_name = full_url + ".jpg"
        save_this = newDir + file_name
        logging.info('Saving: %s', save_this)
        img.save(save_this)
        file_path = "static/icons/" + file_name
        logging.info('File path being uploaded is: %s', file_path)
        executible = "UPDATE sites SET icon_url=  (\"" + str(
            file_path) + "\") WHERE site_url = (\"" + url + "\") "
        database_connection('update_data', executible)
        logging.info('Database:upload_icon: Finished')

database = Database()
url_list = database.original_url_list


class Site(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def check_single(self, url):
        """Pings and http requests a single site.
        Updates database with up or down icon
        status code.

        Keyword arguments:
        url -- the url to be checked
        """
        logging.info('Site:check_single: Started')
        if isinstance(url, unicode):
            ping_item = str(url)
            logging.info('is unicode, ping item now: %s', ping_item)
        else:
            ping_item = str(url[0])
            logging.info('not unicode, ping item now: %s', ping_item)
        http_item = ping_item
        url_item = ping_item
        ping_item_parse = urlparse(ping_item)
        ping_item_hostname = ping_item_parse.hostname
        ping_item_path = ping_item_parse.path
        full_ping_item = ping_item_hostname + ping_item_path
        ping_response = 42
        ping_latency = 5000
        try:
            ping = subprocess.Popen(
                ["ping", "-n", "-c 1", full_ping_item],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = ping.communicate()
            if out:
                try:
                    ping_latency = int(re.findall(r"time=(\d+)", out)[0])
                    ping_response = int(re.findall(
                        r"(\d+) packets received", out)[0])
                    logging.info('Pinging site: %s', full_ping_item)
                    logging.info('Packets received: %s', ping_response)
                    logging.info('Ping latency: %s', ping_latency)
                    logging.info('Time in ms: %s', time)
                except:
                    logging.warning('error occurred finding time')
                    ping_response = 0
                    ping_latency = 'None'

        except subprocess.CalledProcessError:
            logging.warning('check_single: Could not get a ping')
        open_url = urllib.urlopen(http_item)
        final_url = open_url.geturl()
        http_code = open_url.getcode()
        current_time = time.strftime("%x %X")
        logging.info('Final HTTP url: %s', final_url)
        logging.info('HTTP status code: %s', http_code)
        logging.info('Current time: %s', current_time)
        if ping_response == 1 \
                or http_code >= 500 or \
                http_code <= 399 or \
                http_code == 405:
            up_symbol = 9989
            status_icon = up_symbol
        else:
            down_symbol = 10062
            status_icon = down_symbol
        executible = "UPDATE sites SET last_checked=  (\"" + str(
            current_time) + "\"), status_icon= (\"" + str(
            status_icon) + "\"), ping_status= (\"" + str(
            ping_response) + "\"), ping_latency= (\"" + str(
            ping_latency) + "\"), http_status= \"" + str(
            http_code) + "\" WHERE site_url = (\"" + url_item + "\")"
        database_connection('update_data', executible)
        logging.info('Site:check_single: Finished')

    def check_all(self, url_list):
        """Checks status for all sites.

        Keyword arguments:
        url_list -- list of urls to be checked
        """
        logging.info('Site:check_all: Started')
        if len(database.original_url_list) == 0:
            time.sleep(1)
        logging.info('Original database url list: %s',
                     database.original_url_list)
        for url in database.original_url_list:
            self.check_single(url)
        logging.info('Site:check_all: Finished')

site = Site()


def background_status_check():
    """Checks site status in the background"""
    logging.info('background_status_check: Started')
    while True:
        site.check_all(database.original_url_list)
        time.sleep(10)


def background_worker():
    """Opens new thread for checking
    site status in background"""
    logging.info('background_worker: Started')
    database.read_the_table()
    logging.info('Opening new thread')
    background_task = Thread(target=background_status_check)
    background_task.setDaemon(True)
    background_task.start()
    logging.info('background_worker: Finished')

logging.info('Calling background_worker function...')
background_worker()


class App(object):

    @cherrypy.expose
    def index(self):
        """Returns html page."""
        logging.info('App:index: Started')
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
