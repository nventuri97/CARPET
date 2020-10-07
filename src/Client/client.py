#Client for COVID-19 application and to evaluate client anonymous trace

from Crypto.Cipher import AES
from http.client import *

#Example trace
trace='a(-)a(-)s(-)v(-)s(+)s(+)a(+)s(-)s(-)'

#New AES chiper to encrypt the trace that have to send
key=b'Sixteen byte key'
cipher=AES.new(key,AES.MODE_EAX)

#Connection with server