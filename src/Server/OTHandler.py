#Handler to execute the oblivious transfer on a given trace

from http.server import SimpleHTTPRequestHandler
import json
from DFS import DFS
import random

class OTHandler(SimpleHTTPRequestHandler):

    #Transition number
    count=1

    def __init__(self, automata, *args, **kwargs):
        #Automata defined in server which will use
        #to the execution of the OT
        self.automata=automata
        self.mat=self.automata.to_matrix()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        #Execution of OT
        if self.count==1 :
            self.FirstStateTransition()
        else:
            KStateTransition()

    #First subprotocol of the run of OT on automata
    def FirstStateTransition(self):
        Q_len=self.automata.states.__len__-1
        r_a=random.randint(0, Q_len)
        v=[]
        #Blinds element of vector v with the random generated
        for i in range(0,self.automata.alphabet.__len__-1) :
            v[i]=(self.mat[i][0]+r_a)%Q_len

        #Now i have to send the blinds vector to the client
        #and the first transition is done
        self.send_response(200)
        self.send_header('content-type', 'data')
        self.end_headers()
        self.wfile.write(v)

        #Increment the transition number
        self.count+=1

    #Subprotocol for the k-th state transition
    def KStateTransition(self):
        pass