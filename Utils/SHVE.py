from .cryptoUtils import AES_enc, AES_dec, prf
from .BF import BF
from Crypto.Random import get_random_bytes
from Crypto.Util.number import long_to_bytes
from typing import List
from dataclasses import dataclass
import math
import sys

byteorder = sys.byteorder

@dataclass
class s:
    d0: bytes
    d1: bytes
    S: List[int]


class SHVE:
    def __init__(self):
        self.lam = 256  # security parameter
        self.zero_vec = b'0'*((self.lam+math.ceil(math.log2(self.lam)))//8)

    def _xor(self,a:bytes, b: bytes):
        int_a = int.from_bytes(a, byteorder)
        int_b = int.from_bytes(b, byteorder)
        int_enc = int_a ^ int_b
        return int_enc.to_bytes(32, byteorder)

    # gen msk
    def setup(self) -> bytes:
        return get_random_bytes(self.lam//8)

    def keyGenFromBFPos(self, msk: bytes, v: List[int]) -> s:
        """
        input: v is a list that contain all the positions which is 1
        """
        K = get_random_bytes(32)
        d0 = K
        for pos in v:
            d0 = self._xor(prf(msk, long_to_bytes(1) + long_to_bytes(pos)), d0)
        d1 = AES_enc(K, self.zero_vec)
        return s(d0, d1, v)

    def keyGenFromList(self, msk: bytes, v: List[int]) -> s:
        """
        input: v is searched vector
        """
        S = []
        K = get_random_bytes(32)
        d0 = K
        for i, vi in enumerate(v):
            if vi == 1:
                d0 = self._xor(
                    prf(msk, long_to_bytes(vi) + long_to_bytes(i)), d0)
                S.append(i)

        d1 = AES_enc(K, self.zero_vec)
        return s(d0, d1, S)

    def keyGenFromBF(self, msk: bytes, bf: BF) -> s:
        return self.keyGenFromList(msk, list(iter(bf)))

    def encList(self, msk: bytes, x: List[int]) -> List[bytes]:
        """
        input: x is the whole vector
        """
        c = []
        for i, xi in enumerate(x):
            ci = prf(msk, long_to_bytes(xi)+long_to_bytes(i))
            c.append(ci)
        return c

    def encBF(self, msk: bytes, bf: BF) -> List[bytes]:
        return self.encList(msk, list(iter(bf)))

    def query(self, c: List[bytes], s: s):
        for i, pos in enumerate(s.S):
            if i == 0:
                K = c[pos]
            else:
                K = self._xor(c[pos], K)
        K = self._xor(K, s.d0)
        try:
            AES_dec(K, s.d1) == self.zero_vec
        except ValueError:
            return False
        else:
            return True
