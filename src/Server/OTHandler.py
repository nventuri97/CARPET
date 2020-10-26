#Handler to execute the oblivious transfer on a given trace

from http.server import SimpleHTTPRequestHandler
from DFS import DFS
from base64 import b64encode, b64decode
from http.cookies import SimpleCookie
import redis
import numpy as np
import json, random, uuid

from socket import error as SocketError
import errno

class OTHandler(SimpleHTTPRequestHandler):

    #Redis host and redis port
    redis_host='localhost'
    redis_port=6379

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
        #Transition number
        self.k=0
        #Random number array
        self.r_a=[]
        #session uid
        self.suid_str=''
        #Connection to redis database
        self.redis_client=redis.Redis(self.redis_host, self.redis_port)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        cookie=self.headers.get('Cookie')
        #Execution of OT
        if cookie==None :
            self.FirstStateTransition()
        else:
            self.suid_str=cookie[5:]
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
        self.suid_str=cookie['suid'].OutputString()

        #Now i have to send the blinds vector to the client
        #and the first transition is done
        self.send_response(200)
        self.send_header('content-type', 'data')
        self.send_header('Set-Cookie', self.suid_str)
        self.end_headers()
        data={"CardState": self.Q_len, "BlindVector": v}
        data=json.dumps(data, cls=NumpyArrayEncoder).encode()
        self.wfile.write(data)

        #Increment the transition number
        self.k=self.k+1
        self.suid_str=self.suid_str[5:]
        self.__storeData()
        
    
    #Subprotocol for the k-th state transition
    def KStateTransition(self):
        self.__retrieveData()
        self.r_a.append(random.randint(0,self.Q_len))
        print(self.r_a)
        #Blinding all the matrix element
        for i in range(0, self.Q_len):
            for j in range(0, self.Al_len):
                self.mat[i][j]=(self.mat[i][j]+self.r_a[self.k])%self.Q_len
            #Shift left of r_a(k-1) position
            np.roll(self.mat[i], -self.r_a[self.k-1])
        
        #Now i have to read data sent from client
        length = int(self.headers.get('Content-length'))
        data=self.rfile.read(length)
        data=json.loads(data)
        encrypted_v=b64decode(data["ChiperText"])
        print(encrypted_v)
        
        self.__storeData()

    #Store data in redis db to retrive them in the next GET request   
    def __storeData(self):    
        db_data={'r_a': self.r_a, 'k': self.k}
        self.redis_client.hset('session:1', self.suid_str, json.dumps(db_data))

    def __retrieveData(self):
        db_data=json.loads(self.redis_client.hget('session:1', self.suid_str).decode('utf-8'))
        self.r_a=db_data['r_a']
        self.k=db_data['k']


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)