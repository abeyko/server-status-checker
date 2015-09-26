import os, os.path
import cherrypy

class Home:

	@cherrypy.expose
	def index(self):
		return """<html>
			<head>
				<STYLE>
				<!--
				A{text-decoration:none}
				-->
				</STYLE>
				<link href="/static/css/style.css" rel="stylesheet">
			</head>
		<body>
			<h1><a href='/links' style="color: #FFFFFF">Web Service Monitoring <br>Dashboard</br></a></h1>
			<h4><p>By: Angeliki Beyko</p></h4)
		</body>
	</html>"""

	@cherrypy.expose
	def links(self):
		return """<html>
			<head>
				<STYLE>
				<!--
				A{text-decoration:none}
				-->
				</STYLE>
				<link href="/static/css/style.css" rel="stylesheet">
			</head>
		<body>
			<ul>
				<h3><li><a href='/style_1' style="color: #FFFFFF">Style 1</a></li></h3>
				<h3><li><a href='/style_2' style="color: #FFFFFF">Style 2</a></li></h3>
			</ul>
		</body>
		</html>"""

	@cherrypy.expose
	def style_1(self):
		return """<html>
			<head>
				<STYLE>
				<!--
				A{text-decoration:none}
				-->
				</STYLE>
				<link href="/static/css/style.css" rel="stylesheet">
			</head>
		<body>
		<h3>
			<table cellspacing="2" cellpadding="20">
				<tbody>
					<tr><
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Amazon-icon.png"></td>
						<td><a href="http://www.amazon.com" style="color: #FFFFFF">Amazon.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Pinterest-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
					</tr>
					<tr><
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Dropbox-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Reddit-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
					</tr>
					<tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Evernote-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Skype-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
					</tr>
					<tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Facebook-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/StumbleUpon-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
					</tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Flickr-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Tumblr-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
					<tr>
					<tr></tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/GitHub-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Twitter-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
					<tr></tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Instagram-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Vine-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
					<tr></tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/LinkedIn-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Youtube-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td>Status Icon</td>
				</tbody>
			</table>
		</h3>
		</body>
		</html>"""

	@cherrypy.expose
	def style_2(self):
		hostname = "google.com" #example
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
				return hostname, ' is up!'
		else:
				return hostname, ' is down!'


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
 cherrypy.quickstart(Home(), '/', conf)
