#HTTPS Server for COVID-19 application and OT execution

from DFS import DFS
from OTHandler import OTHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import ssl, threading

class ThreadedHTTPSServer(ThreadingMixIn, HTTPServer):
    pass

#Inizialization of DFS and creation of the automata required
states=['0', '1']
automata=DFS(states)

automata.machine.add_transition('a_less', '0', '0')
automata.machine.add_transition('a_plus', '0', '1')
automata.machine.add_transition('s_less', '0', '0')
automata.machine.add_transition('s_plus', '0', '1')
automata.machine.add_transition('v_less', '0', '0')
automata.machine.add_transition('v_plus', '0', '1')
automata.machine.add_transition('a_plus', '1', '1')
automata.machine.add_transition('a_less', '1', '1')
automata.machine.add_transition('s_plus', '1', '1')
automata.machine.add_transition('v_plus', '1', '1')
automata.machine.add_transition('v_less', '1', '1')
automata.machine.add_transition('s_plus', '1', '0')

#Inizialization of HTTPS server
server_address = ('localhost', 4443)
otHandler=OTHandler(automata)
httpd =ThreadedHTTPSServer(server_address, otHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, keyfile='./key.pem', certfile='./cert.pem', ssl_version=ssl.PROTOCOL_TLS)

print("Server is working on port 4443")

httpd.serve_forever()