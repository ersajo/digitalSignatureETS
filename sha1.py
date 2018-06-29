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
        """out = ''
        for x in msg:
            if len(format(ord(x), 'b')) != 8:
                x = '0' * (8 - len(format(ord(x), 'b'))) + format(ord(x), 'b')
            out = out + x
        return out"""

    def binToStr(self, msg):
        return binascii.unhexlify('%x' % int(msg, 2))
        """out = ''
        for x in range(len(msg)/8):
            aux = msg[x*8:(x+1)*8]
            out = out + format(str(msg[x*8:(x+1)*8]))
            print out"""

    def addPadding(self, msg):
        msg = self.strToBin(msg)[2:]
        print self.binToStr(msg)
        if len(msg) % 8 != 0:
            msg = '0' + msg
        msg = msg + '1'
        print len(msg)
        return msg

if __name__ == '__main__':
    sha = SHA1()
    sha.addPadding("abcde")
