#!/usr/bin/env python
# -*- coding utf-8 -*-
import io, socket
from RSA import *
from sha1 import *

def menu():
    print "Introduce una opcion:"
    print "Opcion 1: Generar llaves"
    print "Opcion 2: Firmar documento"
    print "Opcion 3: Verificar documento"
    print "Opcion 4: Envia documento"
    print "Opcion 5: Recibe documento"
    print "Opcion 6: Salir"

def keyGenerator(name):
    rsa = RSA()
    publicKey,privateKey = rsa.genKeys()
    f = io.open('publicKey/public'+name, 'w')
    f.write(unicode(str(publicKey)[1:-1],'utf-8'))
    f.close()
    f = io.open('privateKey/private'+name, 'w')
    f.write(unicode(str(privateKey)[1:-1],'utf-8'))
    f.close()
    print publicKey,privateKey

def signDoc(msg, privateKey, name):
    print "msg: ",msg
    print int(privateKey.split(', ')[0]), int(privateKey.split(', ')[1])
    sha = SHA1()
    rsa = RSA()
    hashed = ''
    for part in range((len(msg)//448)+1):
        hashed = hashed + sha.doDigest(sha.addPadding(msg))
    print "hashed: ", hashed
    cipher = rsa.encrypt(hashed, int(privateKey.split(', ')[0]), int(privateKey.split(', ')[1]))
    out = msg + '\n' + str(cipher)
    print "out: " + str(out)
    f = io.open('cipher'+name+'.txt', 'w')
    f.write(unicode(str(out),'utf-8'))
    f.close()

def verifyDoc(msg, publicKey):
    print "msg: ",msg
    print int(publicKey.split(', ')[0]), int(publicKey.split(', ')[1])
    try:
        n = int(publicKey.split(', ')[0])
        e = int(publicKey.split(', ')[1])
        i = 0
        for char in msg:
            if char == '[':
                break
            i += 1
        out = list()
        for c in msg[i+1:-1].split(","):
            out.append(long(c))
        msg = msg[:i-1]
        rsa = RSA()
        decrypted = rsa.decrypt(out,n,e)
        sha = SHA1()
        hashed = ''
        for part in range((len(msg)//448)+1):
            hashed = hashed + sha.doDigest(sha.addPadding(msg))
        if hashed == decrypted:
            print "MENSAJE AUTENTICO!"
        else:
            print "MENSAJE MODIFICADO!"
    except ValueError:
        print "SE HA INTRODUCIDO UNA LLAVE ERRONEA!"

def sendDoc(route):
    #Cliente
    f = io.open(route,'r')
    message= f.read()
    f.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 10000)
    messageLen = len(message)
    print messageLen
    try:
        sent = sock.sendto(str(messageLen), server_address)
        data, server = sock.recvfrom(4096)
        # Send data
        print 'Enviando "%s"' % message
        sent = sock.sendto(message, server_address)
        # Receive response
        print 'Esperando a recibir'
        data, server = sock.recvfrom(int(messageLen))
        print 'Recibido "%s"' % data

    finally:
        print 'Cerrando socket'
        sock.close()

def receiveDoc():
    #Servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print 'Iniciando en %s puerto %s' % server_address
    sock.bind(server_address)
    messageLen, address = sock.recvfrom(4096)
    sent = sock.sendto("Hecho", address)
    while True:
        print '\nEsperando a recibir un mensaje'
        data, address = sock.recvfrom(int(messageLen))

        print '%s bytes recibidos desde %s' % (len(data), address)
        print data

        if data:
            sent = sock.sendto("Hecho", address)
            print 'Enviando %s bytes de vuelta hacia %s' % (sent, address)
            break
    f = io.open('receiveMessage.txt', 'w')
    f.write(unicode(data,'utf-8'))
    f.close()

while True:
    menu()
    opt = input(">>")
    if opt > 0 and opt < 6:
        if opt == 1:
            name = raw_input("Introduce un nombre\n>>")
            keyGenerator(name)
        if opt == 2:
            idKey = raw_input("Introduce nombre del emisor\n>>")
            route = raw_input("Introduce una ruta de archivo\n>>")

            f = io.open(route,'r')
            msg = f.read()
            f.close()

            f = io.open('privateKey/private'+idKey,'r')
            privateKey = f.read()
            f.close()

            signDoc(msg, privateKey, idKey)
        if opt == 3:
            idKey = raw_input("Introduce nombre del emisor\n>>")
            route = raw_input("Introduce una ruta de archivo\n>>")

            f = io.open(route,'r')
            msg = f.read()
            f.close()

            f = io.open('publicKey/public'+idKey,'r')
            publicKey = f.read()
            f.close()

            verifyDoc(msg, publicKey)
        if opt == 4:
            route = raw_input("Introduce una ruta de archivo\n>>")
            sendDoc(route)
        if opt == 5:
            receiveDoc()
    elif opt == 6:
        exit()
