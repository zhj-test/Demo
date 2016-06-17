#coding:utf-8
import math, time, struct, base64
import urllib.parse
from pyDes import *

class Encrypt:
    ECODE_STR = [0xef, 0x2b, 0xcc, 0xdc, 0x9b, 0x3b, 0xf7, 0x2a, 0x68, 0xad, 0xeb, 0x72, 0xe3, 0x78, 0x2f, 0x5e, 0x7, 0x77, 0xd5, 0xc1, 0x7d, 0x40, 0x66, 0xb8]
    BASE_KEY_SEC = [0xb9, 0x89, 0x84, 0xcf, 0x9f, 0xd0, 0xc5, 0x78, 0x19, 0xe9, 0x56, 0x55, 0xbc, 0x62, 0xda, 0x98, 0x82, 0e8, 0x4c, 0xda, 0x2f, 0xdf, 0xe6, 0x55]
    def IntListToByteList(self, IntList):
        a = IntList[:]
        for i in range(len(a)):
            if a[i]>=128:
                a[i] -= 256
        return a

    def genCroptyKey(self, encodeKeyA, randomStrB):
        result = []
        randomStrB = randomStrB.encode()
        a = self.IntListToByteList(encodeKeyA)
        aLen = len(a)
        bLen = len(randomStrB)
        n = math.ceil(aLen/bLen)
        c = (randomStrB*n)[:aLen]
        for i in range(aLen):
            s = (i+1)%3
            if s==0:
                result.append(a[i]^c[i])
            elif s==1:
                result.append(a[i]&c[i])
            elif s==2:
                result.append(a[i]|c[i])
        return self.IntListToByteList(result)

    def Encrypt(self, params, stamp):
        data = urllib.parse.urlencode(params)
        r = self.genCroptyKey(self.ECODE_STR, stamp)
        k = triple_des(struct.pack('b'*len(r), *r), ECB, '\0\0\0\0\0\0\0\0', pad=None, padmode=PAD_PKCS5)
        d = k.encrypt(data)
        r = base64.standard_b64encode(d).decode()
        return r
