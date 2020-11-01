#Client for COVID-19 application and to evaluate client anonymous trace
from http.client import HTTPSConnection
from base64 import b64encode, b64decode
import hashlib, ssl, json, random
import numpy as np
from phe import paillier

#Example trace
trace=['a(-)','a(-)','s(-)','v(-)','s(+)','s(+)','a(+)','s(-)','s(-)']

#New pailler cipher to encrypt data to send
pubkey, privkey=paillier.generate_paillier_keypair()

ssl._create_default_https_context = ssl._create_unverified_context

#Connection with server
connection=HTTPSConnection('127.0.0.1', 4443)

#First GET request to start the OT run
connection.request('GET', '/')
response=connection.getresponse()
print(response)
data=json.loads(response.read())
Q_len=data["CardState"]
vet=data["BlindVector"]
r_b=vet[0]

#KStateTransition, core of the protocol
for i in trace:
    #Binary vector of Q_len lenght
    binv=np.zeros(Q_len, int)
    binv[r_b]=1
    ciphertext=[pubkey.encrypt(int(x)) for x in binv]
    data={}
    data["PublicKey"]={'n': pubkey.n}
    data["CipherText"]= [(str(x.ciphertext()), x.exponent) for x in ciphertext]
    data["TraceLength"]=len(trace)
    ser_data=json.dumps(data)
    headers={'Content-length': len(ser_data), 'Cookie': response.headers['Set-Cookie']}
    print(headers)
    connection.request('GET', '/', ser_data.encode(), headers=headers)
    print("i'm here: "+str(i))

    #Server's response containing the blinded vector and cardinality of states set
    response=connection.getresponse()
    print(response)
    data=json.loads(response.read())

    en_vet=[paillier.EncryptedNumber(pubkey, int(x[0]), int(x[1])) for x in data['BlindVector']]
    vet=[privkey.decrypt(x) for x in en_vet]
    r_b=vet[0]

for x in vet:
    print(x)

print("i have finished")
connection.close()