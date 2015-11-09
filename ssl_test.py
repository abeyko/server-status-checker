"""try:
    import ssl
except ImportError:
    print "error: no ssl support"""

import httplib
# Remove the / after .com and it works
conn = httplib.HTTPSConnection("www.facebook.com/")
conn.request("HEAD", "/")
res = conn.getresponse()
print res.status, res.reason

data = res.read()
print len(data)
0
data == ''
True
