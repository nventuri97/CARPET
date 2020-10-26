#Client for COVID-19 application and to evaluate client anonymous trace

from Crypto.Cipher import AES
from Crypto import Random
from http.client import HTTPSConnection
from base64 import b64encode, b64decode
import hashlib, ssl, json, random
import numpy as np

#Example trace
trace='a(-)a(-)s(-)v(-)s(+)s(+)a(+)s(-)s(-)'

#New AES chiper to encrypt the trace that have to send
key=''.join(chr(random.randint(0, 0xFF)) for i in range(16))
key = hashlib.sha256(key.encode()).digest()
iv = Random.new().read(AES.block_size)
cipher=AES.new(key,AES.MODE_CBC, iv)

def encrypt(s):
    encryptedString = cipher.encrypt(s)
    return b64encode(encryptedString)

ssl._create_default_https_context = ssl._create_unverified_context

#Connection with server
connection=HTTPSConnection('127.0.0.1', 4443, timeout=10)

#First GET request to start the OT run
connection.request('GET', '/')

#Server's response containing the blinded vector and cardinality of states set
response=connection.getresponse()


data=(response.read())
data=json.loads(data)

Q_len=data["CardState"]
vet=data["BlindVector"]
r_b=vet[0]

#Binary vector of Q_len lenght
binv=np.zeros(Q_len)
binv[r_b]=1
ciphertext= encrypt(binv)
data=json.dumps({"ChiperText": ciphertext.decode('ascii')})
headers={'Content-length': len(data), 'Cookie': response.headers['Set-Cookie']}
print(headers)
connection.request('GET', '/', data.encode(), headers=headers)