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
		return "Work in Progress"

	@cherrypy.expose
	def style_2(self):
		return "Work in Progress"

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
