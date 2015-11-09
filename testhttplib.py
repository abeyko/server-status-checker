import httplib
import ssl
import socket


testurl = "http://www.facebook.com"


def resolve_httpredirect(url, depth=0):
    headers = {"User-Agent": "firefox"}
    body = ""
    print "Depth is " + str(depth)
    if depth > 10:
        raise Exception("Redirected " + depth + "times, giving up.")
    if url.startswith('http://'):
        url = url[7:]
        url = str(url)
        print url + " at depth " + str(depth)
        conn = httplib.HTTPConnection(url)
        req = conn.request("HEAD", "/", body, headers)
        res = conn.getresponse()
        print res.status, res.reason
        headers = dict(res.getheaders())
        if headers.has_key('location') and headers['location'] != url:
            print headers['location']
            return resolve_httpredirect(headers['location'], depth + 1)
    if url.startswith('https://'):
        url = url[8:]
        url = str(url)
        print "print is shttp of " + url + " at depth " + str(depth)
        url = url[:16]
        url = str(url)
        print "new url is " + url
        conn = httplib.HTTPSConnection(url)
        req = conn.request("HEAD", "/", body, headers)
        res = conn.getresponse()
        print res.status, res.reason
        headers = dict(res.getheaders())
        if headers.has_key('location') and headers['location'] != url:
            print "this function called itself through https loop"
            print "https headers loc is " + headers['location']
            return resolve_httpredirect(headers['location'], depth + 1)

resolve_httpredirect(testurl, 0)

"""
########### CODE CEMETARY ################

# METHOD 1 WORKS
conn = httplib.HTTPConnection(testurl)
req = conn.request("HEAD", "/index.html") 
res = conn.getresponse()
reshead = res.getheaders()
for i in reshead:
	print str(i)

#########################

print "fourth print is and final url is " + str(url)

#http = httplib.HTTP(url)

#USER_AGENT = "firefox"

#body = ""

#req = conn.request("HEAD", "/", body, headers)
#http.putheader("User-Agent", USER_AGENT)

print "res is " + str(res)
print res.status, res.reason

o = urlparse.urlparse(self,allow_fragments = True)
conn = httplib.HTTPConnection(o.netloc)
path = o.path
if o.query:
path += '?' + o.query


conn.request("HEAD", path)
new_res = conn.getresponse()
headers = dict(new_res.getheaders())

if headers.has_key('location') and headers['location'] != self:
    return resolve_httpredirect(headers['location'], depth+1)
else:
    return self
    print "url is " + self

#reshead2 = type(reshead)
#print str(reshead)
#print "req is " + str(req) + "is type " + req_type
#req_type = type(req)
#req_type = str(req_type)
#res2 = res.read()
#print "res read is " + str(res2) #+ "and res head is " + str(res3)
#help(res)
#conn.request("HEAD", "/index.html")
#print "conn is " + str(conn)

# gives: conn is <httplib.HTTPConnection instance at 0x1007e7b48>
#req is Noneis type <type 'NoneType'>
resp = urllib2.urlopen(testurl)
resp2 = resp.geturl()
type_resp2 = type(resp2)
print "redirect final is " + str(resp2) + "type is " + str(type_resp2)
#testurl= str(testurl)
resp3 = resp2[7:]
resp3 = str(resp3)
"""
