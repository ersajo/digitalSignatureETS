#!/usr/bin/env python
# -*- coding utf-8 -*-
from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(("127.0.0.1", 8000))

while True:
    mensaje = raw_input("Mensaje a enviar\n>>>")
    clientSocket.send(mensaje)
    if mensaje == 'close':
        break

print 'Adios.'
clientSocket.close()
