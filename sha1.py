#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii


#Rotacion circular a la izquierda leftRotate(1100,0)->1001 para 16 bits
def leftRotate(x,n, w=32):
    while len(x) != w:
        x = '0' + x
    x = x[n:] + x[:n]
    x = '0b' + x
    return int(x,2)

class SHA1(object):

    def __init__(self):
        self.h = [0x67452301,
                  0xEFCDAB89,
                  0x98BADCFE,
                  0x10325476,
                  0xC3D2E1F0
                 ]

    #convierte una cadena a una cadena binaria
    def strToBin(self, msg):
        return bin(int(binascii.hexlify(msg), 16))

    #convierte una cadena binaria a un numero hexadecimal
    def binToHex(self, msg):
        return hex(int(msg, 2))

    #se hace utiliza un relleno de ceros de acuerdo al estandar marcado por el RFC 3174
    def addPadding(self, msg=""):
        if len(msg) != 0:
            msg = self.strToBin(msg)[2:]
        while len(msg) % 8 != 0:
            msg = '0' + msg
        lenMsg = hex(len(msg))[2:]
        while len(lenMsg) != 16:
            lenMsg = '0' + lenMsg
        msg = msg + '1'
        while len(msg) % 448 != 0:
            msg = msg + '0'
        msg = (self.binToHex(msg)[:-1] + lenMsg +'L')[2:-1]
        return msg

    def f1(self,B,C,D):
        return (B & C) | (~(B) & D)

    def f2(self,B,C,D):
        return B ^ C ^ D

    def f3(self,B,C,D):
        return (B & C) ^ (B & D) ^ (C & D)

    def f4(self,B,C,D):
        return B ^ C ^ D

    @property
    def k1(self):
        return 0x5A827999

    @property
    def k2(self):
        return 0x6ED9EBA1

    @property
    def k3(self):
        return 0x8F1BBCDC

    @property
    def k4(self):
        return 0xCA62C1D6

    #Se ejecuta el algoritmo de sha1
    def doDigest(self, msg):
        self.words = list()
        for i in range(16):
            self.words.append(int(msg[8*i:8*(i+1)], 16))
        for t in range(16, 80):
            aux = self.words[t-3] ^ self.words[t-8] ^ self.words[t-14] ^ self.words[t-16]
            word = leftRotate(bin(aux)[2:],1)
            self.words.append(word)
        A = self.h[0]; B = self.h[1]; C = self.h[2]; D = self.h[3]; E = self.h[4];
        for t in range(80):
            if t >= 0 and t <=19:
                temp = (leftRotate(bin(A)[2:],5) + self.f1(B,C,D) + E + self.words[t] + self.k1) & 2**32-1
            elif t >= 20 and t <=39:
                temp = (leftRotate(bin(A)[2:],5) + self.f2(B,C,D) + E + self.words[t] + self.k2) & 2**32-1
            elif t >= 40 and t <=59:
                temp = (leftRotate(bin(A)[2:],5) + self.f3(B,C,D) + E + self.words[t] + self.k3) & 2**32-1
            elif t >= 60 and t <=79:
                temp = (leftRotate(bin(A)[2:],5) + self.f4(B,C,D) + E + self.words[t] + self.k4) & 2**32-1
            E = D
            D = C
            C = leftRotate(bin(B)[2:],30)
            B = A
            A = temp
        self.h[0] = (self.h[0] + A) & 2**32-1
        self.h[1] = (self.h[1] + B) & 2**32-1
        self.h[2] = (self.h[2] + C) & 2**32-1
        self.h[3] = (self.h[3] + D) & 2**32-1
        self.h[4] = (self.h[4] + E) & 2**32-1
        out = str(hex(self.h[0]))[2:-1] + str(hex(self.h[1]))[2:-1] + str(hex(self.h[2]))[2:-1] + str(hex(self.h[3]))[2:-1] + str(hex(self.h[4]))[2:-1]
        return out

if __name__ == '__main__':
    sha = SHA1()
    print sha.doDigest(sha.addPadding('abcde'))
