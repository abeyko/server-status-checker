import cherrypy
import os
import sqlite3
#import requests
import httplib
import urlparse
import urllib2
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

            # METHOD 1 - gets status code, but needs to do redirect

            http_item = item[0]
            if http_item.startswith('http://'):
                http_item = http_item[7:]
                http_item = str(http_item)
                print http_item
                print "http_item " + http_item
                print type(http_item)
                response = httplib.HTTPConnection(http_item)  # new code works
                # w/out the str(), it gives error saying cannot concoctenate
                # str + instance objects
                print "response is " + str(response)
                response.request("HEAD", http_item)
                #response = httplib.HTTPMessage(http_item)
                # print "response with message is " + str(response)
                new_response = response.getresponse()
                print "new response is " + str(new_response)
                status_code = new_response.status
                print "status code is " + str(status_code)
            """ 

                ## METHOD 2 - attempt at redirecting
            http_item = item[0]
            depth = 0
            if http_item.startswith('http://'):
                http_item = http_item[7:]
                print "http_item " + str(http_item)
                o = urlparse.urlparse(http_item,allow_fragments = True)
                print "o is " + str(o)
                conn = httplib.HTTPConnection(o.netloc)
                print "conn is " + str(conn)
                path = o.path
                print "path is " + str(path)

                #query = len(o.query)
                #print "o.query is of length " + str(query)
                #print "o.query is " + str(o.query) + "before the if"
                #if o.query:
                 #   path += '?' + o.query
                #print "o.query is " + str(o.query) + "after the if"
                #print "o.query is of length " + str(query)

                conn.request("HEAD", path)
                new_res = conn.getresponse()
                print "new_res is " + str(new_res)
                headers = dict(new_res.getheaders())
                print "headers is " + str(headers)
                if headers.has_key('location') and headers['location'] != http_item:
                    print "if statement" + str(resolve_httpredirect(headers['location'], depth+1))
                    print "depth is " + str(depth)
                else:
                    print "else statement " + str(http_item)

                """
            # METHOD 3 urllib to get final url and then put through httplib
            """
            resp = urllib2.urlopen(item[0])
            url_response = resp.geturl()
            print "url_response is " + str(url_response)


            
            http_item = url_response
            if http_item.startswith('http://'):
                http_item = http_item[7:]
                http_item = str(http_item)
                print http_item
                print "http_item " + http_item
                print type(http_item)
                response = httplib.HTTPConnection(http_item) # new code works
                print "response is " + str(response) # w/out the str(), it gives error saying cannot concoctenate str + instance objects
                response.request("HEAD", http_item)
                #response = httplib.HTTPMessage(http_item)
                #print "response with message is " + str(response)
                #new_response = response.getresponse(response)
                #print "new response is " + str(new_response)
                status_code = new_response.status
                print "status code is " + str(status_code)




                
                def resolve_httpredirect(url, depth=0):
                    if depth > 10:
                        raise Exception("Redirected " + depth + "times, giving up.")
                        o = urlparse.urlparse(url,allow_fragments = True)
                        conn = httplib.HTTPConnection(o.netloc)
                        path = o.path
                        if o.query:
                            path += '?' + o.query
                        conn.request("HEAD", path)
                        new_res = conn.getresponse()
                        headers = dict(new_res.getheaders())
                        if headers.has_key('location') and headers['location'] != url:
                            return resolve_httpredirect(headers['location'], depth+1)
                        else:
                            return url
                            print "url is " + url
                """

            #status = response.getresponse()
            # print "status is " + str(status)
            ##new_response = response.request("HEAD", "/index.html")
            # print "new response is " + str(new_response)
            #response2 = httplib.HTTPConnection.request(response)

            # message = httplib.HTTPResponse(response) # gives error: AttributeError: HTTPConnection instance has no attribute 'makefile'
            # print "message is " + str(message)
            # try to use httplib instead of requests
            #http_response = response.status_code
            # print response.status_code, response.url
            # if ping_response == 0 or http_response == 200:
            #http_status_check = httplib.responses[200]
            if ping_response == 0:
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
