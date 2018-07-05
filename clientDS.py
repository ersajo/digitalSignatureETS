#!/usr/bin/env python
# -*- coding utf-8 -*-
from socket import *
import io
from RSA import *
from sha1 import *

rsa = RSA()
sha = SHA1()
publicKey,privateKey = rsa.genKeys()
f = io.open('file.txt','r')
text = f.read()
print "text: ",text
f.close()
hashed = ''
print "len(text): ", len(text)
for part in range(len(text)//448+1):
    hashed = hashed + sha.doDigest(sha.addPadding(text))
print "hashed: ", hashed
cipher = rsa.encrypt(hashed,privateKey[0], privateKey[1])
f = io.open('cipher.txt', 'w', encoding='utf-8')
for c in cipher:
    f.write(unicode(str(c),'utf-8'))
f.close()
print "len(text|cipher): ",len(text + '|' + str(cipher))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(("127.0.0.1", 8000))
print "publica, privada: ", publicKey,privateKey
clientSocket.send(str(len(text + '|' + str(cipher))))
clientSocket.send(text + '|' + str(cipher))
clientSocket.send(str(publicKey))

while True:
    mensaje = raw_input("Mensaje a enviar\n>>>")
    clientSocket.send(mensaje)
    if mensaje == 'close':
        break
print 'Adios.'
clientSocket.close()
