#Handler to execute the oblivious transfer on a given trace

from http.server import SimpleHTTPRequestHandler
from DFS import DFS
from base64 import b64encode, b64decode
from http.cookies import SimpleCookie
import redis
import numpy as np
import json, random, uuid
from phe import paillier    
from socket import error as SocketError

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
        #trace length
        self.t_len=0
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
        v=np.zeros(self.Al_len, int)
        #Blinds element of vector v with the random generated
        for i in range(0,self.Al_len):
            v[i]=(self.mat[i][0]+self.r_a[self.k])%self.Q_len

        #Setting session cookie
        suid=uuid.uuid4()
        print(suid)
        cookie=SimpleCookie()
        cookie['suid']=suid
        self.suid_str=(cookie['suid'].OutputString())[5:]

        #Now i have to send the blinds vector to the client
        #and the first transition is done
        
        data={"CardState": self.Q_len, "BlindVector": v}
        self.__sendResponse(data)

        #Increment the transition number
        self.__storeData()
        
    
    #Subprotocol for the k-th state transition
    def KStateTransition(self):
        self.__retrieveData()
        self.r_a.append(random.randint(0,self.Q_len))
        print(self.r_a)
        #Blinding all the matrix element
        for i in range(0, self.Al_len):
            for j in range(0, self.Q_len):
                self.mat[i][j]=(self.mat[i][j]+self.r_a[self.k])%self.Q_len
            #Shift left of r_a(k-1) position
            np.roll(self.mat[i], -self.r_a[self.k-1])
        
        #Now i have to read data sent from client
        length = int(self.headers.get('Content-length'))
        data=self.rfile.read(length)
        recive_data=json.loads(data)
        self.t_len=recive_data['TraceLength']
        puk=recive_data['PublicKey']
        public_key=paillier.PaillierPublicKey(n=int(puk['n']))
        encrypted_e=[paillier.EncryptedNumber(public_key, int(x[0]), int(x[1])) for x in recive_data['CipherText']]

        #v is the encrypted vector obtained by multiplicating transition matrix to encrypted vector recived
        enc_mean=np.mean(encrypted_e)
        v_encrypt=np.dot(self.mat, encrypted_e)

        data={}
        data["BlindVector"]= [(str(x.ciphertext()), x.exponent) for x in v_encrypt]
        self.__sendResponse(data)

        self.k=self.k+1
        self.__storeData()

    def announceResult(self):
        f=np.zeros(self.Q_len, int)
        for j in range(self.Q_len):
            ind=(j+self.r_a[self.k])%self.Q_len
            f[ind]=j

        data={}
        data["BlindVector"]=f
        print(f)
        self.__sendResponse(data)
        
    #Store data in redis db to retrive them in the next GET request   
    def __storeData(self):    
        db_data={'r_a': self.r_a, 'k': self.k}
        self.redis_client.hset('session:1', self.suid_str, json.dumps(db_data))

    def __retrieveData(self):
        db_data=json.loads(self.redis_client.hget('session:1', self.suid_str).decode('utf-8'))
        self.r_a=db_data['r_a']
        self.k=db_data['k']

    def __sendResponse(self, data):
        self.send_response(200)
        self.send_header('content-type', 'data')
        self.send_header('Set-Cookie', 'suid='+self.suid_str)
        self.end_headers()
        if self.k==0 or self.k==9:
            self.wfile.write(json.dumps(data, cls=NumpyArrayEncoder).encode())
        else:
            self.wfile.write(json.dumps(data).encode())

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)