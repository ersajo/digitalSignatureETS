#!/usr/bin/env python
#  coding utf-8
import binascii


#Rotacion circular a la izquierda leftRotate(1100,0)->1001 para 16 bits
def leftRotate(i,n):
    return ((i << n) & 0xFFFFFFFF) | (i >> (32-n))

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

    #convierte una cadena binaria a una cadena
    def binToStr(self, msg):
        return binascii.unhexlify('%x' % int(msg, 2))

    #convierte una cadena binaria a un numero hexadecimal
    def binToHex(self, msg):
        return hex(int(msg, 2))

    #convierte un numero hexadecimal en una cadena
    def hexToStr(self, msg):
        return ''.join([chr(int(''.join(c), 16)) for c in zip(msg[0::2],msg[1::2])])

    #convierte una cadena a un numero hexadecimal
    def strToHex(self, msg):
        return hex(int(self.strToBin(msg), 2))

    #se hace utiliza un relleno de ceros de acuerdo al estandar marcado por el RFC 3174
    def addPadding(self, msg=""):
        if len(msg) != 0:
            msg = self.strToBin(msg)[2:]
        if len(msg) % 8 != 0:
            msg = '0' + msg
        lenMsg = hex(len(msg))[2:]
        while len(lenMsg) != 16:
            lenMsg = '0' + lenMsg
        msg = msg + '1'
        while len(msg) % 448 != 0:
            msg = msg + '0'
        msg = (self.binToHex(msg)[:-1] + lenMsg +'L')[2:-1]
        return msg

    def notBin(self, bin):
        aux = ''
        for char in str(bin)[2:]:
            if char == '0':
                aux = aux + '1'
            elif char == '1':
                aux = aux + '0'
        aux = '0b' + aux
        return int(aux, 2)

    @property
    def f1(self):
        return (self.h[1] & self.h[2]) | (self.notBin(bin(self.h[1])) & self.h[4])

    @property
    def f2(self):
        return self.h[1] ^ self.h[2] ^ self.h[3]

    @property
    def f3(self):
        return (self.h[1] & self.h[2]) | (self.h[1] & self.h[3]) | (self.h[2] & self.h[3])

    @property
    def f4(self):
        return self.h[1] ^ self.h[2] ^ self.h[3]

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
            self.words.append(int(msg[8*i:8*(i+1)]))

        for t in range(16, 80):
            binAux = self.words[t-3] ^ self.words[t-8] ^ self.words[t-14] ^ self.words[t-16]
            word = leftRotate(binAux,1)
            self.words.append(word)
        for t in range(80):
            if t >= 0 and t <=19:
                temp = leftRotate(self.h[0],5) + self.f1 + self.h[4] + self.words[t] + self.k1
            elif t >= 20 and t <=39:
                temp = leftRotate(self.h[0],5) + self.f2 + self.h[4] + self.words[t] + self.k2
            elif t >= 40 and t <=59:
                temp = leftRotate(self.h[0],5) + self.f3 + self.h[4] + self.words[t] + self.k3
            elif t >= 60 and t <=79:
                temp = leftRotate(self.h[0],5) + self.f4 + self.h[4] + self.words[t] + self.k4

            self.h[4] = self.h[3]
            self.h[3] = self.h[2]
            self.h[2] = leftRotate(self.h[1],30)
            self.h[1] = self.h[0]
            self.h[0] = temp

        print self.h


    @property
    def getWords(self):
        return self.words

if __name__ == '__main__':
    print 0xda39a3ee5e6b4b0d3255bfef95601890afd80709
    sha = SHA1()
    sha.doDigest(sha.addPadding(''))
