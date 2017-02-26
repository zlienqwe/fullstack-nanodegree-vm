from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppy_shelter import Base, Puppy, Shelter

engine = create_engine('sqlite:///puppy_shelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


def filterPuppy(self):
	thisPuppyId = self.path.split('/')[2]
	puppyQuery = session.query(Puppy).filter_by(id=thisPuppyId).one()
	return puppyQuery

class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('/puppys'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			allPuppyList = session.query(Puppy).order_by(Puppy.id.desc())
			
			output = ""
			output += "<html><body>"

			output += "<a href='/puppys/add'>add new puppy</a><br>"
			for puppy in allPuppyList:
				output += puppy.name
				output += '<br>'
				output += "<a href='/puppy/%s/edit'>edit</a>" % str(puppy.id) 
				output += '<br>'
				output += "<a href='/puppy/%s/delete'>delete</a>"% str(puppy.id)
				output += '<br>'
				output += "<br>"
			output += "</body></html>"
			self.wfile.write(output)
		elif self.path.endswith('/puppys/add'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += 'add a new puppy!'
			output += "<form method='POST' enctype='multipart/form-data' action='/puppys/add'>"
			output += "<input name='addPuppyName' placeholder='add...' type='text' >"
			output += "<input type='radio' value='male' name='gender'> boy"
			output += "<input type='radio' value='female' name='gender'> girl"
			output += "<input type='submit' value='Submit'>"
			output += '</form></body></html>'

			self.wfile.write(output)
		elif self.path.endswith('/edit'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			thisPuppyId = self.path.split('/')[2]
			puppyQuery = session.query(Puppy).filter_by(id=thisPuppyId).one()
			output = ""
			output += "<html><body>"
			output += 'edit this puppy %s!' % puppyQuery.name
			output += "<form method='POST' enctype='multipart/form-data' action='/puppy/%s/edit'>" % thisPuppyId
			output += "<input name='editPuppyName' placeholder='edit...' type='text' >"
			output += "<input type='submit' value='Submit'>"
			output += '</form></body></html>'
			self.wfile.write(output)
		elif self.path.endswith('/delete'):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.end_headers()
			thisPuppyId = self.path.split('/')[2]
			puppyQuery = session.query(Puppy).filter_by(id=thisPuppyId).one()
			output = ""
			output += "<html><body>"
			output += 'delete this puppy %s!' % puppyQuery.name
			output += "<form method='POST' enctype='multipart/form-data' action='/puppy/%s/delete'>" % thisPuppyId
			output += "<input type='submit' value='Submit'>"
			output += '</form></body></html>'
			self.wfile.write(output)
	def do_POST(self):
		try:
			if self.path.endswith('/add'):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('addPuppyName')
					gender = fields.get('gender')

					newPuppy = Puppy(name=messagecontent[0], gender=gender[0])
					session.add(newPuppy)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/puppys')
					self.end_headers()
			elif self.path.endswith('/edit'):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('editPuppyName')
					
					puppyQuery = filterPuppy(self)
					
					puppyQuery.name = messagecontent[0]
					session.add(puppyQuery)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/puppys')
					self.end_headers()
			elif self.path.endswith('/delete'):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)

					puppyQuery = filterPuppy(self)

					session.delete(puppyQuery)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/puppys')
					self.end_headers()
		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(("", port), WebServerHandler)
		print "puppy webserver is running."
		server.serve_forever()
	except KeyboardInterrupt:
		print "entered, stopping puppy webserver..."
		server.socket.close()

if __name__ == '__main__':
	main()
