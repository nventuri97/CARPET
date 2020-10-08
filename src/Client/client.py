#Client for COVID-19 application and to evaluate client anonymous trace

from Crypto.Cipher import AES
from http.client import HTTPSConnection
import json

#Example trace
trace='a(-)a(-)s(-)v(-)s(+)s(+)a(+)s(-)s(-)'

#New AES chiper to encrypt the trace that have to send
key=b'Sixteen byte key'
cipher=AES.new(key,AES.MODE_EAX)

#Connection with server
connection=HTTPSConnection('127.0.0.1', 4443, timeout=10)
if ConnectionError :
    print("Something went wrong, try later")

#Encrypted trace needed to execute OT
cipher_text, tag= cipher.encrypt_and_digest(trace)
data=json.dumps({"encrypt_trace":cipher_text, "len":cipher_text.__len__})
connection.send(data)

