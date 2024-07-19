from Crypto.Random import get_random_bytes
from .cryptoUtils import prf, hash_length
from dataclasses import dataclass
from Crypto.Util.number import long_to_bytes
import random
import math


@dataclass
class HValue:
    b: int
    L: bytes
    K: bytes


class TSet:
    def __init__(self, n: int, k: int):
        '''
        n: Number of inserted elements
        k: expansion factor
        '''
        self._cal_BS(n, k)
        self.t_set = [[b""]*self.S for _ in range(self.B)]

    def _cal_BS(self, n: int, k: int):
        N = n*k
        logN = math.ceil(math.sqrt(N))
        self.B = logN
        self.S = logN

    # (w,id) -> (b,L,K)
    def _hash_func(self, stag: bytes, i: int) -> HValue:
        tmp = hash_length(prf(stag, long_to_bytes(i)), 3)
        h = HValue(int.from_bytes(tmp[:4], 'big') %
                   self.B, tmp[4:12], tmp[12:120])
        return h

    # TSet[b]: whether the corresponding list is free
    def _free_b(self, b: int):
        l_b = self.t_set[b]
        while b"" in l_b:
            j = random.randint(0, self.S-1)
            if l_b[j] == b"":
                return j
        else:
            raise Exception("insufficient space")

    def _xor(self, a: bytes, b: bytes) -> bytes:
        return bytes([ai ^ bi for ai, bi in zip(a, b)])

    def setup(self, T: dict):
        kt = get_random_bytes(16)
        for w, t in T.items():
            stag = prf(kt, w)
            beta = 1  # if the current id is the last one in t
            for i in range(1, len(t)+1):
                h = self._hash_func(stag, i)

                j = self._free_b(h.b)
                if i == len(t):
                    beta = 0
                s = t[i-1]
                s = bytearray(s)
                s.insert(0, beta)
                value = self._xor(s, h.K)
                self.t_set[h.b][j] = h.L+value
        return kt

    def retrive(self, stag: bytes):
        t = []
        beta = 1
        i = 1
        while beta == 1:
            h = self._hash_func(stag, i)
            for lv in self.t_set[h.b]:
                if not lv:
                    continue
                if lv[:8] == h.L:
                    s = self._xor(lv[8:], h.K)
                    beta = s[0]
                    t.append(s[1:])
            i += 1

            if len(t) == 0:
                break
        return t


def genStag(kt: bytes, w: str) -> bytes:
    return prf(kt, w)


# Calculate the memory size of useful data in TSet
def cal_size(tset: TSet) -> int:
    size = 0
    for pair_lst in tset.t_set:
        for pair in pair_lst:
            if pair != b"":
                size += len(pair)
    return size
