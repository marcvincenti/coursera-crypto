#!/usr/bin/env python

from Crypto.Hash import SHA256

""" Message Authentication Cipher
Our goal in this project is to build a file authentication system that lets
browsers authenticate and play video chunks as they are downloaded without
having to wait for the entire file. Instead of computing a hash of the entire
file, the web site breaks the file into 1KB blocks (1024 bytes). It computes the
hash of the last block and appends the value to the second to last block. It
then computes the hash of this augmented second to last block and appends the
resulting hash to the third block from the end.

Now, a browser downloads the file F one block at a time, where each block
includes the appended hash value from the diagram above. When the first block
(B0 || h_1) is received the browser checks that H(B0 || h_1) is equal to h_0 and
if so it begins playing the first video block. When the second block (B1 || h_2)
is received the browser checks that H(B1 || h_2) is equal to h_1 and if so it
lays this second block. This process continues until the very last block. This
way each block is authenticated and played as it is received and there is no
need to wait until the entire file is downloaded.

It is not difficult to argue that if the hash function H is collision resistant
then an attacker cannot modify any of the video blocks without being detected by
the browser. Indeed, since h_0 = H(B0 || h_1) an attacker cannot find a pair
(B0', h_1') != (B0, h_1) such that h_0 = H(B0' || h_1') since this would break
collision resistance of H. Therefore after the first hash check the browser is
convinced that both B0 and h_1 are authentic. Exactly the same argument proves
that after the second hash check the browser is convinced that both B1 and h_2
are authentic, and so on for the remaining blocks.
"""

def read_in_chunks(file_path, chunk_size=1024):
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def get_file_chunks(file_path, chunk_size=1024):
    chunks = []
    for c in read_in_chunks(file_path):
        chunks.append(c)
    return chunks

previous_hash = None
for chunk in reversed(get_file_chunks("6.1.intro.mp4")):
    sha = SHA256.new()
    sha.update(chunk)
    if previous_hash:
        sha.update(previous_hash)
    previous_hash = sha.digest()

print(sha.hexdigest())
