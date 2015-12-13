import cherrypy
import os
import sqlite3
import httplib
import time


class App(object):

    @cherrypy.expose
    def index(self):
        return open("./public/Site Monitoring Dashboard.html",
                    'r').read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def popular_sites_data(self):
        """Return the site and icon urls
        of the popular_sites database."""
        connection = sqlite3.connect('sqlite3.db')
        connection = connection.cursor()
        connection.execute("SELECT site_url FROM popular_sites")
        popular_sites_site_url_result = connection.fetchall()
        popular_sites_site_url_result = list(popular_sites_site_url_result)
        connection.execute("SELECT icon_url FROM popular_sites")
        popular_sites_icon_url_result = connection.fetchall()
        popular_sites_icon_url_result = list(popular_sites_icon_url_result)
        connection.close()
        return {
            'site_url': popular_sites_site_url_result,
            'icon_url': popular_sites_icon_url_result
        }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def my_sites_data(self):
        """Return the site urls of the
        popular_sites database."""
        connection = sqlite3.connect('sqlite3.db')
        connection = connection.cursor()
        connection.execute("SELECT site_url FROM my_sites")
        my_sites_site_url_result = connection.fetchall()
        my_sites_site_url_result = list(my_sites_site_url_result)
        connection.close()
        return {
            'site_url': my_sites_site_url_result
        }

    @cherrypy.expose
    def add_site(self, add_site):
        """Add site to my_sites database.

        Keyword arguments:
        add_site -- the url of the site to be added
        """
        with sqlite3.connect('sqlite3.db') as connection:
            cherrypy.session['ts'] = time.time()
            connection.execute("INSERT INTO my_sites VALUES (?, ?)",
                               [cherrypy.session.id, add_site])

    @cherrypy.expose
    def delete_site(self, delete_site):
        """Delete site from my_sites database.

        Keyword arguments:
        delete_site -- the url of the site to be deleted
        """
        with sqlite3.connect('sqlite3.db') as connection:
            connection.execute("DELETE FROM my_sites WHERE Site_Url=?",
                               [delete_site])

    @cherrypy.expose
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
        """Return the status icon after checking each url
        in the popular_sites and my_sites tables."""
        connection = sqlite3.connect('sqlite3.db')
        print "Connected to sqlite3 db"
        connection = connection.cursor()
        connection.execute("SELECT site_url FROM popular_sites")
        popular_sites_site_url_result = connection.fetchall()
        popular_sites_site_url_result = list(popular_sites_site_url_result)
        connection.execute("SELECT site_url FROM my_sites")
        my_sites_site_url_result = connection.fetchall()
        my_sites_site_url_result = list(my_sites_site_url_result)
        connection.close()
        result_list = []
        merged_db_tables = popular_sites_site_url_result + \
            my_sites_site_url_result
        for item in merged_db_tables:
            ping_item = item[0]
            http_item = item[0]
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
