#HTTPS Server for COVID-19 application and OT execution

from DFS import DFS
from OTHandler import OTHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn
from functools import partial
import ssl

class ThreadedHTTPSServer(ThreadingMixIn, HTTPServer):
    pass

#Inizialization of DFS and creation of the automata required
states=['0', '1']
automata=DFS(states)

#transition form (name method, source state, destination state, conditions to call the method)
automata.machine.add_transition('a_less', '0', '0', 'a(-)')
automata.machine.add_transition('a_plus', '0', '1', 'a(+)')
automata.machine.add_transition('s_less', '0', '0', 's(-)')
automata.machine.add_transition('s_plus', '0', '1', 's(+)')
automata.machine.add_transition('v_less', '0', '0', 'v(-)')
automata.machine.add_transition('v_plus', '0', '1', 'v(+)')
automata.machine.add_transition('a_plus', '1', '1', 'a(+)')
automata.machine.add_transition('a_less', '1', '1', 'a(-)')
automata.machine.add_transition('s_plus', '1', '1', 's(+)')
automata.machine.add_transition('v_plus', '1', '1', 'v(+)')
automata.machine.add_transition('v_less', '1', '1', 'v(-)')
automata.machine.add_transition('s_less', '1', '0', 's(-)')

#Inizialization of HTTPS server
server_address = ('localhost', 4443)
otHandler=partial(OTHandler, automata)
httpd =ThreadedHTTPSServer(server_address, otHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, keyfile='./key.pem', certfile='./cert.pem', ssl_version=ssl.PROTOCOL_TLS)

print("Server is working on port 4443")

httpd.serve_forever()