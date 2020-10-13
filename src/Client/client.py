#Client for COVID-19 application and to evaluate client anonymous trace

from Crypto.Cipher import AES
from Crypto import Random
from http.client import HTTPSConnection
import json
import hashlib, ssl

#Example trace
trace='a(-)a(-)s(-)v(-)s(+)s(+)a(+)s(-)s(-)'

#New AES chiper to encrypt the trace that have to send
key='Sixteen byte key'
key = hashlib.sha256(key.encode()).digest()
iv = Random.new().read(AES.block_size)
cipher=AES.new(key,AES.MODE_CBC, iv)

ssl._create_default_https_context = ssl._create_unverified_context

#Connection with server
connection=HTTPSConnection('127.0.0.1', 4443, timeout=10)
if ConnectionError :
    print("Something went wrong, try later")

#First GET request to start the OT run
connection.request('GET', '/')

#Server's response containing the blinded vector
response=connection.getresponse()
vet=(response.read())
r_b=vet[0]