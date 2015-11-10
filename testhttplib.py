import httplib

testurl = "http://www.facebook.com"


def resolve_httpredirect(url, depth=0):
    headers = {"User-Agent": "firefox"}
    body = ""
    if depth > 10:
        raise Exception("Redirected " + depth + "times, giving up.")
    if url.startswith('http://'):
        print "------------------START-------------------"
        print "LEVEL: " + str(depth)
        print "URL: " + url
        url = url[7:]
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

    req = conn.request("HEAD", "/", body, headers)
    res = conn.getresponse()
    print "STATUS: " + str(res.status)
    print "REASON: " + str(res.reason)

    headers = dict(res.getheaders())
    if 'location' in headers and headers['location'] != url:
        print "NEW LOCATION: " + headers['location']
        print "-----------------------------------------"
        return resolve_httpredirect(headers['location'], depth + 1)
    else:
        print "-----------------FINISH-------------------"
        print " "


resolve_httpredirect(testurl, 0)
