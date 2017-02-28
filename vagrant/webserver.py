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
				output += "<b>%s</b>" % restaurant.name
				output += '<br>'
				output += "<a style='margin-right: 15px; color: #5fb7c1; text-decoration: none;' href='/restaurants/%s/edit'>edit</a>    " % str(restaurant.id)
				output += "<a style='text-decoration: none; color: red;' href='/restaurants/%s/delete'>delete</a>" % str(restaurant.id)
				output += "</h3>"
				output += '<br>'
			output += "<br><br><br><a href='/restaurants/create'>create a new restaurant</a>"
			output += "</body></html>"
			self.wfile.write(output)
			return
		elif self.path.endswith('/restaurants/create'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += "<h1>Hello!</h1>"
			output += "<h2>please add a new restaurant</h2>"
			output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
			output += "<input name='newRestaurantName' placeholder='new restaurent name' type='text' >"
			output += "<input type='submit' value='Submit'>"
			output += '</form></body></html>'
			self.wfile.write(output)
		elif self.path.endswith('/edit'):
			restaurantId = self.path.split('/')[2]
			editRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantId).one()
			if editRestaurantQuery:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += "<h2>edit this restaurant!!</h2>"
				output += "<h3>%s</h3>" % editRestaurantQuery.name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % editRestaurantQuery.id
				output += "<input name='thisRestaurantName' placeholder='restaurent name edit' type='text' >"
				output += "<input type='submit' value='Submit'>"
				output += '</form></body></html>'
				self.wfile.write(output)

		elif self.path.endswith('/delete'):
			restaurantId = self.path.split('/')[2]

			deleteRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantId).one()
			if deleteRestaurantQuery:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += "<h2>delete this restaurant!!</h2>"
				output += "<h3 style='color: red'>are u sure u want to delete restaruant %s ?</h3>" % deleteRestaurantQuery.name
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % deleteRestaurantQuery.id
				output += "<input type='submit' value='Submit'>"
				output += '</form></body></html>'
				self.wfile.write(output)

		else:
			self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

					newRestaruant = Restaurant(name = messagecontent[0])
					session.add(newRestaruant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
			elif self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('thisRestaurantName')
					thisRestaurantId = self.path.split('/')[2]


					thisRestaurantQuery = session.query(Restaurant).filter_by(id=thisRestaurantId).one()
					if thisRestaurantQuery != []:
						thisRestaurantQuery.name = messagecontent[0]

						session.add(thisRestaurantQuery)
						session.commit()

						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

			elif self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					thisRestaurantId = self.path.split('/')[2]

					thisRestaurantQuery = session.query(Restaurant).filter_by(id=thisRestaurantId).one()
					session.delete(thisRestaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
		except:
			pass

def main():
	try:
		port = 9999
		server = HTTPServer(('', port), WebServerHandler)
		print 'webserver runing on port %s' % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^c entered, stopping webserver..."
		server.socket.close()



if __name__ == '__main__':
	main()
