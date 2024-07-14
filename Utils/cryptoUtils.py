from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hmac
from hashlib import sha256

'''
crypto
'''
def prf(k:bytes,m)->bytes:
    if not (type(m) is bytes):
        m = bytes(m, 'utf-8')
    p = hmac.new(k,m,digestmod=sha256)
    return p.digest()

def hash(m)->bytes:
    if not (type(m) is bytes):
        m = bytes(m, 'utf-8')
    return sha256(m).digest()

def hash_length(msg, int: int):
    h = hash(msg)
    i = 0
    while i < int:
        h = hash(msg+bytes(str(i), "utf-8"))+h
        i = i+1
    return h

# AES/CBC
def AES_enc(key: bytes, m) -> bytes:
    if not (type(m) is bytes):
        m = bytes(m, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    c = cipher.encrypt(pad(m, AES.block_size))
    return iv+c


def AES_dec(key: bytes, c: bytes) -> bytes:
    iv = c[:AES.block_size]
    c = c[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    m = cipher.decrypt(c)
    return unpad(m, AES.block_size)
