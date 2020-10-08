#Handler to execute the oblivious transfer on a given trace

from http.server import SimpleHTTPRequestHandler
import json
from DFS import DFS

class OTHandler(SimpleHTTPRequestHandler):

    def __init__(self, automata):
        #Automata defined in server which will use
        #to the execution of the OT
        self.automata=automata

    def do_GET(self):
        #JSON parsin of request
        json_string=self.requestline
        data=json.loads(json_string)
        ot_trace=data[0]
        lenght=data[1]

        #Execution of OT
        OTExecution(ot_trace)



    def OTExecution(self, trace):
        pass