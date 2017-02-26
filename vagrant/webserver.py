from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path.endswith('/restaurants'):
			restaurants = session.query(Restaurant).all()
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += "<h1>Hello!</h1>"
			output += "<h2>Here is the list of restaurants:</h2>"
			for restaurant in restaurants:
				output += "<h3>"
				output += restaurant.name
				output += "</h3>"
			output += "</body></html>"
			self.wfile.write(output)
			print output
			return
			
		elif self.path.endswith('/hola'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += "<h1>Hello!</h1>"
			output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
			output += "</body></html>"
			self.wfile.write(output)
			return
		else:
			self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type'))
			print ctype
			print pdict
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
			output = ""
			output += "<html><body>"
			output += " <h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
			output += "</body></html>"
			self.wfile.write(output)
			print output

		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), WebServerHandler)
		print 'webserver runing on port %s' % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^c entered, stopping webserver..."
		server.socket.close()



if __name__ == '__main__':
	main()
