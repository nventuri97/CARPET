#HTTPS Server for COVID-19 application and OT execution

from DFS import DFS
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

#Inizialization of HTTPS server
server_address = ('localhost', 4443)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='./cert.pem', ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()

