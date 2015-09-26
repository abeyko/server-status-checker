import cherrypy

class Home:

	@cherrypy.expose
	def index(self):
		return "<a href='/links'>Web Service Monitoring Dashboard</a>"

	@cherrypy.expose
	def links(self):
		return """
		<ul>
			<li><a href='/style_1'>Style 1</a></li>
			<li><a href='/style_2'>Style 2</a></li>
		</ul>
		"""

	@cherrypy.expose
	def style_1(self):
		return "Work in Progress"

	@cherrypy.expose
	def style_2(self):
		return "Work in Progress"

home = Home()
cherrypy.quickstart(home)