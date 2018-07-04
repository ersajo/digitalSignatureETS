#!/usr/bin/env python
# -*- coding utf-8 -*-
from socket import *
from RSA import *
from sha1 import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 8000))

serverSocket.listen(1)
(clientSocket, address) = serverSocket.accept()
longitud = clientSocket.recv(1024)
print "longitud: ", longitud
string = clientSocket.recv(int(longitud))
publicKey = clientSocket.recv(1024)
print "publicKey: ", publicKey
print "string: ", string
n = int(publicKey[1:-1].split(",")[0])
e = int(publicKey[1:-1].split(",")[1])
out = list()
print "len(string): ", len(string)
cipher = string.split('|')[1]
original = string.split('|')[0]
print "original: ", original
for c in cipher[1:-1].split(","):
    out.append(long(c))
rsa = RSA()
decrypted = rsa.decrypt(out,n,e)
print ''
print str(address[0]) + " envio: " + original + '#' + decrypted
sha = SHA1()
hashed = ''
for part in range(len(original)//448+1):
    hashed = hashed + sha.doDigest(sha.addPadding(original))
print "hashed:", hashed
if hashed == decrypted:
    print "Mensaje autentico"
else:
    print "Mensaje modificado"

while True:
    recibido = clientSocket.recv(1024)
    if recibido == 'close':
        break

    print str(address[0]) + " dice: ", recibido

    clientSocket.send(recibido)

print "Adios."
clientSocket.close()
serverSocket.close()
