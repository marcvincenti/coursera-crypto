#!/usr/bin/env python

""" Padding Oracle
In this project you will experiment with a padding oracle attack against a toy
web site hosted at crypto-class.appspot.com . Padding oracle vulnerabilities
affect a wide variety of products, including secure tokens .

Now to business. Suppose an attacker wishes to steal secret information from our
target web site crypto-class.appspot.com . The attacker suspects that the web
site embeds encrypted customer data in URL parameters such as this:
http://crypto-class.appspot.com/po?er=f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4

That is, when customer Alice interacts with the site, the site embeds a URL like
this in web pages it sends to Alice. The attacker intercepts the URL listed
above and guesses that the ciphertext following the "po?er=" is a hex encoded
AES CBC encryption with a random IV of some secret data about Alice's session.
"""

import urllib2
import sys

#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def __init__(self):
		self.target_url = "http://crypto-class.appspot.com/po?er="

    def query(self, q):
        target = self.target_url + urllib2.quote(q)
        req = urllib2.Request(target)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            # print "We got: %d" % e.code
            if e.code == 404:
                return True
            return False

#--------------------------------------------------------------
# main
#--------------------------------------------------------------
def hex_xor_128(a, b):
    return "{0:032x}".format(int(a,base=16) ^ int(b,base=16))

if __name__ == "__main__":
    po = PaddingOracle()

    target_data = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
    target_data = target_data.decode('hex')

    cipher_blocks = [target_data[i:i+16] for i in range(0, len(target_data), 16)]
    final_messages = [""]*(len(cipher_blocks)-1)
    print "".join(final_messages)

    # we iterate through each cipher block by starting at the first block (+iv)
    for block_number, pred_cipher_block in enumerate(cipher_blocks[0:-1]):
        message_block = []
        print "----- block {0} ------".format(block_number)
        # we try to guess every byte by starting at the end of the block
        for padding, byte in enumerate(pred_cipher_block[::-1], 1):
            # we create a padding depending on wich byte we are trying to guess
            custom_pad = "00"*(16-padding) + ("{0:02x}".format(padding))*padding
            for guess in range(128):
                unmodified_preceding_blocks = ''.join(cipher_blocks[0:block_number]).encode('hex')
                custom_block = (pred_cipher_block[0:16-padding] + chr(ord(byte)^guess) + "".join(message_block)).encode('hex')
                req_string = unmodified_preceding_blocks + hex_xor_128(custom_block, custom_pad) + cipher_blocks[block_number+1].encode('hex')
                if (po.query(req_string)):
                    print "found => 0x{0:02x}".format(guess)
                    message_block.insert(0, chr(ord(byte)^guess))
                    if 32 <= guess < 128:
                        final_messages[block_number] = chr(guess) + final_messages[block_number]
                    break
                if guess == 127:
                    print "failed"
                    # It seems that one of the padding byte is failing
                    message_block.insert(0, chr(ord(byte)^9))
        print final_messages[block_number]
    print "".join(final_messages)
