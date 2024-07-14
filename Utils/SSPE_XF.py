from dataclasses import dataclass
from typing import List
import math
from Crypto.Random import get_random_bytes
from .cryptoUtils import prf
from .XorFilter import XorFilter,get_pos
import sys

byteorder = sys.byteorder


@dataclass
class s:
    sk1: bytes
    sk2: bytes
    S: List[int]


@dataclass
class MSK:
    # secret key
    sk: bytes
    # xorfilter related parameters
    k: int
    m: int
    seed: int = 0


@dataclass
class MSK_XF:
    msk: MSK
    xf: XorFilter


class SSPE_XF:
    def __init__(self):
        lam = 256
        self.zero_vec = b'0'*((lam+math.ceil(math.log2(lam)))//8)

    def _xor(self,a:bytes, b: bytes):
        int_a = int.from_bytes(a, byteorder)
        int_b = int.from_bytes(b, byteorder)
        int_enc = int_a ^ int_b
        return int_enc.to_bytes(32, byteorder)

    # gen msk
    def setup(self, n: int) -> MSK_XF:
        sk = get_random_bytes(32)
        xf = XorFilter(n)
        m = xf.s
        k = 3
        msk = MSK(sk, k, m)
        return MSK_XF(msk, xf)

    # gen query key
    def keyGen(self, msk: MSK, X: List[str]) -> s:
        K = get_random_bytes(32)
        sk2 = prf(K,self.zero_vec)
        
        sk1 = K
        tmps = [prf(msk.sk, x) for x in X]
        S = get_pos(tmps, msk.k, msk.m, msk.seed)
        for tmp in tmps:
            sk1 = self._xor(sk1, tmp)
        return s(sk1, sk2, S)

    # gen ct: ct = msk_bf.xf
    def enc(self, msk_bf: MSK_XF, Y: List[str]):
        msk = msk_bf.msk
        xf = msk_bf.xf
        
        tmps = [prf(msk.sk, y) for y in Y]
        xf.update(tmps)
        msk.seed = xf.get_seed()

        
    def dec(self, s: s, ct: XorFilter) -> bool:
        xor_res = s.sk1
        for idx in s.S:
            xor_res = self._xor(ct.array[idx], xor_res)
        K = xor_res
        return s.sk2 == prf(K,self.zero_vec)