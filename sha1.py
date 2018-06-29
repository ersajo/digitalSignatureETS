#!/usr/bin/env python
#  coding utf-8
import binascii

class SHA1(object):

    def __init__(self):
        self.h = [0x67452301,
                  0xEFCDAB89,
                  0x98BADCFE,
                  0x10325476,
                  0xC3D2E1F0
                 ]

    def strToBin(self, msg):
        return bin(int(binascii.hexlify(msg), 16))

    def binToStr(self, msg):
        return binascii.unhexlify('%x' % int(msg, 2))

    def binToInt(self, msg):
        return binascii.unhexlify('%x' % int(msg, 16))

    def addPadding(self, msg):
        msg = self.strToBin(msg)[2:]
        print len(msg)
        if len(msg) % 8 != 0:
            msg = '0' + msg
        msg = msg + '1'
        while len(msg) % 448 != 0:
            msg = msg + '0'
        print hex(int(msg, 2))
        return msg

if __name__ == '__main__':
    sha = SHA1()
    sha.addPadding("abcde")
