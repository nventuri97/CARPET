#Handler to execute the oblivious transfer on a given trace

from http.server import SimpleHTTPRequestHandler
from DFS import DFS
import numpy as np
import json
import random

class OTHandler(SimpleHTTPRequestHandler):

    #Transition number
    k=0
    #Random number array
    r_a=[]

    def __init__(self, automata, *args, **kwargs):
        #Automata defined in server which will use
        #to the execution of the OT
        self.automata=automata
        self.mat=self.automata.to_matrix()
        #Cardinality of states set
        self.Q_len=len(self.automata.states)
        #Cardinality of alphabet
        self.Al_len=len(self.automata.alphabet)
        random.seed()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        #Execution of OT
        if self.k==0 :
            self.FirstStateTransition()
        else:
            self.KStateTransition()

    #First subprotocol of the run of OT on automata
    def FirstStateTransition(self):
        self.r_a.append(random.randint(0, self.Q_len))
        v=np.zeros(self.Q_len, int)
        #Blinds element of vector v with the random generated
        for i in range(0,self.Q_len):
            v[i]=(self.mat[i][0]+self.r_a[self.k])%self.Q_len

        #Now i have to send the blinds vector to the client
        #and the first transition is done
        self.send_response(200)
        self.send_header('content-type', 'data')
        self.end_headers()
        data={"CardState": self.Q_len, "BlindVector": v}
        data=json.dumps(data, cls=NumpyArrayEncoder).encode()
        self.wfile.write(data)

        #Increment the transition number
        self.k+=1

    #Subprotocol for the k-th state transition
    def KStateTransition(self):
        self.r_a.append(random.randint(0,self.Q_len))
        #Blinding all the matrix element
        for i in range(0, self.Q_len):
            for j in range(0, self.Al_len):
                self.mat[i][j]=(self.mat[i][j]+r_a[k])%self.Q_len
            #Shift left of r_a(k-1) position
            np.roll(mat[i], -self.r_a[k-1])
        
        #Now i have to read data sent from client
        data=self.requestline()


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)