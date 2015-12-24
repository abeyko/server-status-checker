import sqlite3

connection = sqlite3.connect('sqlite3.db')


print 'URL LIST'
print url_list
"""

#print 'ICON LIST'
#print icon_list
#print 'LAST CHECKED LIST'
#print last_checked_list
#print 'PING STATUS'
#print ping_status_list
#print 'PING LATENCY'
#print ping_latency_list
#print 'HTTP STATUS'
#print http_status_list


connection.execute("SELECT site_url FROM my_sites")
my_sites_site_url_result = connection.fetchall()
connection.close()
return {
    'site_url': my_sites_site_url_result
}
#print "here is table: "
#print table
#return table
"""