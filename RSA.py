#! /usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
from os import *
from random import *

class RSA(object):

    def strToBin(self, msg):
        return bin(int(binascii.hexlify(msg), 16))

    def strToHex(self, msg):
        return binascii.hexlify(msg)

    def strToInt(self, msg):
        return int(binascii.hexlify(msg), 16)

    def isPrime(self, n):
        for i in range(2, (int(n ** 0.5) + 1)):
            if n % i == 0:
                return False
        return True

    def genPrime(self):
        while True:
            val = self.strToInt(urandom(1))
            if self.isPrime(val):
                return val

    def invMult(self, e, phi):
        d = 0
        x1 = 0
        x2 = 1
        y1 = 1
        temp_phi = phi

        while e > 0:
            temp1 = temp_phi/e
            temp2 = temp_phi - temp1 * e
            temp_phi = e
            e = temp2

            x = x2- temp1* x1
            y = d - temp1 * y1

            x2 = x1
            x1 = x
            d = y1
            y1 = y

        if temp_phi == 1:
            return d + phi

    def genKeys(self):
        try:
            p = self.genPrime()
            q = self.genPrime()
            n = p*q
            phiEuler = (p-1)*(q-1)
            while True:
                e = randint(1,phiEuler)
                if self.mcd(phiEuler, e) == 1:
                    break
            d = self.invMult(e, phiEuler)
            return (n,e),(n,d)
        except ValueError:
            print "HA OCURRIDO UN ERROR, INTENTA DE NUEVO!"

    def mcd(self, a, b):
        if b==0:
            return a
        else:
            return self.mcd(b, a%b)

    def encrypt(self, msg, n, e):
        return [(ord(char) ** e) % n for char in msg]

    def decrypt(self, msg, n, d):
        return ''.join([chr((char ** d) % n) for char in msg])

if __name__ == "__main__":
    rsa = RSA()
    publicKey,privateKey = rsa.genKeys()
    print publicKey,privateKey
    cipher = rsa.encrypt("Hola",privateKey[0], privateKey[1])
    print cipher
    print rsa.decrypt(cipher,publicKey[0], publicKey[1])
