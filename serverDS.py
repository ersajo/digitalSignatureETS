#!/usr/bin/env python
# -*- coding utf-8 -*-
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 8000))

serverSocket.listen(1)
(clientSocket, address) = serverSocket.accept()

while True:
    recibido = clientSocket.recv(1024)
    if recibido == 'close':
        break

    print str(address[0]) + " dice: ", recibido

    clientSocket.send(recibido)

print "Adios."
clientSocket.close()
serverSocket.close()
