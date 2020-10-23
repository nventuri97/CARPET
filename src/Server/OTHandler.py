#Handler to execute the oblivious transfer on a given trace

from http.server import SimpleHTTPRequestHandler
from DFS import DFS
from base64 import b64encode, b64decode
from http.cookies import SimpleCookie
import redis
import numpy as np
import json, random, uuid

class OTHandler(SimpleHTTPRequestHandler):

    #Redis host and redis port
    redis_host='localhost'
    redis_port=6379
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
        self.redisconn=redis.StrictRedis(host=self.redis_host, port=self.redis_port, password="", decode_responses=True)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        #cookie=self.headers.get('Cookie')
        #suid=cookie['suid']
        #Execution of OT
        if self.k==0:
            self.FirstStateTransition()
        else:
            print("i'm here")
            self.KStateTransition()


    #First subprotocol of the run of OT on automata
    def FirstStateTransition(self):
        self.r_a.append(random.randint(0, self.Q_len))
        v=np.zeros(self.Q_len, int)
        #Blinds element of vector v with the random generated
        for i in range(0,self.Q_len):
            v[i]=(self.mat[i][0]+self.r_a[self.k])%self.Q_len

        #Setting session cookie
        suid=uuid.uuid4()
        print(suid)
        cookie=SimpleCookie()
        cookie['suid']=suid

        #Now i have to send the blinds vector to the client
        #and the first transition is done
        self.send_response(200)
        self.send_header('content-type', 'data')
        self.send_header('Set-Cookie', cookie['suid'].OutputString())
        self.end_headers()
        data={"CardState": self.Q_len, "BlindVector": v}
        data=json.dumps(data, cls=NumpyArrayEncoder).encode()
        self.wfile.write(data)

        #Increment the transition number
        self.k=self.k+1
        print(self.k)

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
        data=b64decode(data)
        e=data["ChiperText"]

        


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)