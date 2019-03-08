#!/usr/bin/env python

from Crypto.Cipher import AES
from Crypto.Util import Counter

""" AES
In this project you will implement two encryption/decryption systems,
one using AES in CBC mode and another using AES in counter mode (CTR).
In both cases the 16-byte encryption IV is chosen at random and is prepended to the ciphertext.
"""

cbc_key = "140b41b22a29beb4061bda66b6747e14"
cbc_cipher1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
cbc_cipher2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"

def cbc_decrypt(key, cipher):
    dec_cipher = cipher.decode('hex')
    aes_cbc = AES.new(key.decode('hex'), AES.MODE_CBC, dec_cipher[:16])
    return aes_cbc.decrypt(dec_cipher[16:])

print cbc_decrypt(cbc_key, cbc_cipher1)
print cbc_decrypt(cbc_key, cbc_cipher2)

ctr_key = "36f18357be4dbd77f050515c73fcf9f2"
ctr_cipher1 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
ctr_cipher2 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"

def ctr_decrypt(key, cipher):
    dec_cipher = cipher.decode('hex')
    ctr = Counter.new(128, initial_value=int(cipher[:32], 16))
    aes_ctr = AES.new(key.decode('hex'), AES.MODE_CTR, counter=ctr)
    return aes_ctr.decrypt(dec_cipher[16:])

print ctr_decrypt(ctr_key, ctr_cipher1)
print ctr_decrypt(ctr_key, ctr_cipher2)
