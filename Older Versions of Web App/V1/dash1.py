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
			<h5>
			<P STYLE="border: double #CCFFCC 20px">
			<a href='/style_1' style="color: #FFFFFF">Style 1</a><br>
			<a href='/style_2' style="color: #FFFFFF">Style 2</a></br>
			</P>			
			</h5>
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
			<meta http-equiv='content-type' content='text/html; charset=utf-8'>
<title>Web Service Monitoring Dashboard</title>
<script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js'></script>
<script type='text/javascript'>
  $(document).ready(function()
  {
    $('button').on('click', function()
    {
      var request = $.ajax({'url': '/getData'});
      request.done(function(response) 
      {
        $('#amazon').text(response.amazon);
        $('#dropbox').text(response.dropbox);
        $('#evernote').text(response.evernote);
        $('#facebook').text(response.facebook);
        $('#flickr').text(response.flickr);
        $('#github').text(response.github);
        $('#instagram').text(response.instagram);
        $('#linkedin').text(response.linkedin);
        $('#pinterest').text(response.pinterest);
        $('#reddit').text(response.reddit);
        $('#skype').text(response.skype);
        $('#stumbleupon').text(response.stumbleupon);
        $('#tumblr').text(response.tumblr);
        $('#twitter').text(response.twitter);
        $('#vine').text(response.vine);
        $('#youtube').text(response.youtube);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite1'});
      request.done(function(response) 
      {
        $('#amazon').text(response.amazon);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite2'});
      request.done(function(response) 
      {
        $('#dropbox').text(response.dropbox);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite3'});
      request.done(function(response) 
      {
        $('#evernote').text(response.evernote);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite4'});
      request.done(function(response) 
      {
        $('#facebook').text(response.facebook);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite5'});
      request.done(function(response) 
      {
        $('#flickr').text(response.flickr);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite6'});
      request.done(function(response) 
      {
        $('#github').text(response.github);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite7'});
      request.done(function(response) 
      {
        $('#instagram').text(response.instagram);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite8'});
      request.done(function(response) 
      {
        $('#linkedin').text(response.linkedin);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite9'});
      request.done(function(response) 
      {
        $('#pinterest').text(response.pinterest);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite10'});
      request.done(function(response) 
      {
        $('#reddit').text(response.reddit);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite11'});
      request.done(function(response) 
      {
        $('#skype').text(response.skype);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite12'});
      request.done(function(response) 
      {
        $('#stumbleupon').text(response.stumbleupon);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite13'});
      request.done(function(response) 
      {
        $('#tumblr').text(response.tumblr);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite14'});
      request.done(function(response) 
      {
        $('#twitter').text(response.twitter);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite15'});
      request.done(function(response) 
      {
        $('#vine').text(response.vine);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
      var request = $.ajax({'url': '/pingSite16'});
      request.done(function(response) 
      {
        $('#youtube').text(response.youtube);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
    })
  });
</script>
			</head>
		<body>
		<h3>
			<button>Ping the sites!</button>
			<table cellspacing="2" cellpadding="20" align="center" STYLE="border: double #CCFFCC 20px">
				<tbody>
					<tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Amazon-icon.png"></td>
						<td><a href="http://www.amazon.com" style="color: #FFFFFF">Amazon.com</a></td>
						<td><div id='amazon'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Pinterest-icon.png"></td>
						<td><a href="http://www.pinterest.com" style="color: #FFFFFF">Pinterest.com</a></td>
						<td><div id='pinterest'></div></td>
					</tr>
					<tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Dropbox-icon.png"></td>
						<td><a href="http://www.dropbox.com" style="color: #FFFFFF">Dropbox.com</a></td>
						<td><div id='dropbox'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Reddit-icon.png"></td>
						<td><a href="http://www.reddit.com" style="color: #FFFFFF">Reddit.com</a></td>
						<td><div id='reddit'></div></td>
					</tr>
					<tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Evernote-icon.png"></td>
						<td><a href="http://www.evernote.com" style="color: #FFFFFF">Evernote.com</a></td>
						<td><div id='evernote'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Skype-icon.png"></td>
						<td><a href="http://www.skype.com" style="color: #FFFFFF">Skype.com</a></td>
						<td><div id='skype'></div></td>
					</tr>
					<tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Facebook-icon.png"></td>
						<td><a href="http://www.facebook.com" style="color: #FFFFFF">Facebook.com</a></td>
						<td><div id='facebook'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/StumbleUpon-icon.png"></td>
						<td><a href="http://www.stumbleupon.com" style="color: #FFFFFF">Stumbleupon.com</a></td>
						<td><div id='stumbleupon'></div></td>
					</tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Flickr-icon.png"></td>
						<td><a href="http://www.flickr.com" style="color: #FFFFFF">Flickr.com</a></td>
						<td><div id='flickr'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Tumblr-icon.png"></td>
						<td><a href="http://www.tumblr.com" style="color: #FFFFFF">Tumblr.com</a></td>
						<td><div id='tumblr'></div></td>
					<tr>
					<tr></tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/GitHub-icon.png"></td>
						<td><a href="http://www.github.com" style="color: #FFFFFF">Github.com</a></td>
						<td><div id='github'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Twitter-icon.png"></td>
						<td><a href="http://www.twitter.com" style="color: #FFFFFF">Twitter.com</a></td>
						<td><div id='twitter'></div></td>
					<tr></tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Instagram-icon.png"></td>
						<td><a href="http://www.instagram.com" style="color: #FFFFFF">Instagram.com</a></td>
						<td><div id='instagram'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Vine-icon.png"></td>
						<td><a href="http://www.vine.co" style="color: #FFFFFF">Vine.co</a></td>
						<td><div id='vine'></div></td>
					<tr></tr>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/LinkedIn-icon.png"></td>
						<td><a href="http://www.linkedin.com" style="color: #FFFFFF">Linkedin.com</a></td>
						<td><div id='linkedin'></div></td>
						<td width="64" align="center"><img src="http://icons.iconarchive.com/icons/lunartemplates/modern-social-media-circles/64/Youtube-icon.png"></td>
						<td><a href="http://www.youtube.com" style="color: #FFFFFF">Youtube.com</a></td>
						<td><div id='youtube'></div></td>
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

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def getData(self):
		return {
			'amazon' : 'Pinging Site...',
			'dropbox' : 'Pinging Site...',
			'evernote' : 'Pinging Site...',
			'facebook' : 'Pinging Site...',
			'flickr' : 'Pinging Site...',
			'github' : 'Pinging Site...',
			'instagram' : 'Pinging Site...',
			'linkedin' : 'Pinging Site...',
			'pinterest' : 'Pinging Site...',
			'reddit' : 'Pinging Site...',
			'skype' : 'Pinging Site...',
			'stumbleupon' : 'Pinging Site...',
			'tumblr' : 'Pinging Site...',
			'twitter' : 'Pinging Site...',
			'vine' : 'Pinging Site...',
			'youtube' : 'Pinging Site...'
		}

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite1(self):
		hostname = "amazon.com" #example website, sidenote: amazon blocks pings, maybe fall to something simpler like wget
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
				'amazon' : 'is up!'
			}
		else:
			return {
			 	'amazon' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite2(self):
		hostname = "dropbox.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			 	'dropbox' : 'is up!'
			}
		else:
			return {
			 	'dropbox' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite3(self):
		hostname = "evernote.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
				'evernote' : 'is up!'
			}
		else:
			return {
				'evernote' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite4(self):
		hostname = "facebook.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'facebook' : 'is up!'
			}
		else:
			return {
			  'facebook' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite5(self):
		hostname = "flickr.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'flickr' : 'is up!'
			}
		else:
			return {
			  'flickr' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite6(self):
		hostname = "github.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'github' : 'is up!'
			}
		else:
			return {
			  'github' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite7(self):
		hostname = "instagram.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'instagram' : 'is up!'
			}
		else:
			return {
			  'instagram' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite8(self):
		hostname = "linkedin.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'linkedin' : 'is up!'
			}
		else:
			return {
			  'linkedin' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite9(self):
		hostname = "pinterest.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'pinterest' : 'is up!'
			}
		else:
			return {
			  'pinterest' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite10(self):
		hostname = "reddit.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'reddit' : 'is up!'
			}
		else:
			return {
			  'reddit' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite11(self):
		hostname = "skype.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'skype' : 'is up!'
			}
		else:
			return {
			  'skype' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite12(self):
		hostname = "stumbleupon.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'stumbleupon' : 'is up!'
			}
		else:
			return {
			  'stumbleupon' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite13(self):
		hostname = "tumblr.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'tumblr' : 'is up!'
			}
		else:
			return {
			  'tumblr' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite14(self):
		hostname = "twitter.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'twitter' : 'is up!'
			}
		else:
			return {
			  'twitter' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite15(self):
		hostname = "vine.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'vine' : 'is up!'
			}
		else:
			return {
			  'vine' : 'is down!'
			} 
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def pingSite16(self):
		hostname = "youtube.com" 
		response = os.system("ping -c 1 " + hostname)

		#and then check the response...
		if response == 0:
			return {
			  'youtube' : 'is up!'
			}
		else:
			return {
			  'youtube' : 'is down!'
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
cherrypy.quickstart(Home(), '/', conf)
