#Client for COVID-19 application and to evaluate client anonymous trace
from http.client import HTTPSConnection
from base64 import b64encode, b64decode
import hashlib, ssl, json, random
import numpy as np
from phe import paillier

#Example trace, list of finite character from the alphabet
#trace=['a(-)','a(-)','s(-)','v(-)','s(+)','s(+)','a(+)','s(+)','s(+)','s(-)']
trace=['a(-)','a(-)','s(-)','v(-)','v(+)','v(+)','a(+)','s(+)','s(+)','s(+)']

print(trace)

enc_trace=[]
#Ecoding of the trace needed to address the array
#we choose number from 0 to 5 following the order of the alphabet
for i in trace:
    if i=='a(-)':
        enc_trace.append(0)
    elif i=='a(+)':
        enc_trace.append(1)
    elif i=='s(-)':
        enc_trace.append(2)
    elif i=='s(+)':
        enc_trace.append(3)
    elif i=='v(-)':
        enc_trace.append(4)
    elif i=='v(+)':
        enc_trace.append(5)

#New pailler cipher to encrypt data to send
pubkey, privkey=paillier.generate_paillier_keypair()

ssl._create_default_https_context = ssl._create_unverified_context

#Connection with server
connection=HTTPSConnection('127.0.0.1', 4443)
print(connection)

headers={'TraceLength': len(trace)}
#First GET request to start the OT run
connection.request('GET', '/', headers=headers)

response=connection.getresponse()
print(response)
data=json.loads(response.read())
#Cardinality of the set of states
Q_len=data["CardState"]
#Blinded vector
vet=data["BlindVector"]
r_b=vet[enc_trace[0]]

print("#####First transition#####\n---Blinded vector receive---")
print(vet)

#KStateTransition, core of the protocol
for i in enc_trace[1:]:
    print("#####K-th transition#####")
    print("i'm here: "+str(i))
    #Binary vector of Q_len lenght
    binv=np.zeros(Q_len, int)
    binv[r_b]=1

    print("---Binary vector send---")
    print(binv)

    #Encryption of the data to send to the server
    ciphertext=[pubkey.encrypt(int(x)) for x in binv]

    data={}
    data["PublicKey"]={'n': pubkey.n}
    data["CipherText"]= [(str(x.ciphertext()), x.exponent) for x in ciphertext]
    ser_data=json.dumps(data)

    #Headers={
    #   Content-length: length of the data to send
    #   Cookie: the suid sent by the server to identify the client
    #   Result: boolean flag that indicates the end of the protocol
    #}
    headers={'Content-length': len(ser_data), 'Cookie': response.headers['Set-Cookie'], 'Result': False}
    connection.request('GET', '/', ser_data.encode(), headers=headers)

    #Server's response containing the blinded vector and cardinality of states set
    response=connection.getresponse()
    data=json.loads(response.read())

    #Rebuild and decryption of the data received from the previous request
    en_vet=[paillier.EncryptedNumber(pubkey, int(x[0]), int(x[1])) for x in data['BlindVector']]
    vet=[privkey.decrypt(x) for x in en_vet]
    print("---Vector receive---")
    print(vet)
    r_b=vet[i]

#Last GET request that communicates the end of the trace of the user
headers={'Content-length': 0, 'Cookie': response.headers['Set-Cookie'], 'Result': True}
connection.request('GET', '/', headers=headers)

#Response containing the result of the OT protocol
response=connection.getresponse()
data=json.loads(response.read())
f=data["BlindVector"]
print("#####Result#####")
print(f[r_b])

print("I have finished")
connection.close()