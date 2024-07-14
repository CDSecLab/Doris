"""
ConjFilter that support single keyword search
"""

from Crypto.Random import get_random_bytes
from typing import List
import struct
from Utils.cryptoUtils import prf, AES_enc, AES_dec
from Utils.TSet import TSet, genStag
from Utils.fileUtils import read_index
from dataclasses import dataclass


@dataclass
class PARAMS:
    kt: bytes = get_random_bytes(16)
    kx: bytes = get_random_bytes(16)
    kp: bytes = get_random_bytes(16)
    kenc: bytes = get_random_bytes(16)
    msk: bytes = None


class EDB:
    def __init__(self, n: int, k: int) -> None:
        self.k = k
        self.EMM = TSet(n, k)  # tset
        self.X = set()  # xset

    def setup(self, fpath_wid: str, fpath_idw: str, keys:PARAMS):
        MM = dict()

        dct_wid = read_index(fpath_wid)
        dct_idw = read_index(fpath_idw)

        # TSet
        for word_a, lst_a in dct_wid.items():
            t = []
            kt_a = prf(keys.kt, word_a)
            k_enc_a = prf(keys.kp, word_a)

            for id in lst_a:
                tag_av = prf(kt_a, id)
                etag_av = AES_enc(k_enc_a, tag_av)
                ev_v = AES_enc(keys.kenc, id)
                element = struct.pack("H", len(etag_av)) + etag_av + ev_v
                t.append(element)
                # XSet
                # The rest of the w under that id
                ws = dct_idw.get(id).copy() # Copy to prevent the w from being deleted
                ws.remove(word_a)
                for word_b in ws:
                    kx_ab = prf(keys.kx, word_a + word_b)
                    self.X.add(prf(kx_ab, tag_av))

            MM[word_a] = t
        keys.msk = self.EMM.setup(MM)


"""
Complete search process
"""


def search(ws: List[str], edb: EDB,keys: PARAMS) -> List[int]:
    # token
    stag = genStag(keys.msk, ws[0])
    k_enc_w1 = prf(keys.kp, ws[0])
    kxs = []
    for i in range(1, len(ws)):
        kx_i = prf(keys.kx, ws[0] + ws[i])
        kxs.append(kx_i)

    # tset&xset
    t = edb.EMM.retrive(stag)

    end = []
    for item in t:
        (l,) = struct.unpack("H", item[:2])
        etag_l = item[2 : 2 + l]
        ev_l = item[2 + l :]
        tag_l = AES_dec(k_enc_w1, etag_l)

        for d in range(1, len(ws)):
            dtag_ld = prf(kxs[d - 1], tag_l)
            if dtag_ld not in edb.X:
                break
        else:
            ind = AES_dec(keys.kenc, ev_l)
            end.append(ind)

    return end


"""
every step
"""


@dataclass
class TOKEN:
    stag: bytes
    k_enc_w1: bytes
    kxs: List[bytes]


def c_gen_token(ws: List[str],keys: PARAMS) -> TOKEN:
    stag = genStag(keys.msk, ws[0])
    k_enc_w1 = prf(keys.kp, ws[0])
    kxs = []
    for i in range(1, len(ws)):
        kx_i = prf(keys.kx, ws[0] + ws[i])
        kxs.append(kx_i)
    return TOKEN(stag, k_enc_w1, kxs)


def s_search(token: TOKEN, edb: EDB) -> List[bytes]:
    t = edb.EMM.retrive(token.stag)
    enc_res = []

    for item in t:
        # start = time()
        (l,) = struct.unpack("H", item[:2])
        etag_l = item[2 : 2 + l]
        ev_l = item[2 + l :]
        tag_l = AES_dec(token.k_enc_w1, etag_l)

        flag = 0
        d_num = len(token.kxs)
        for d in range(d_num):
            dtag_ld = prf(token.kxs[d], tag_l)
            if dtag_ld in edb.X:
                flag += 1
        if flag == d_num:
            enc_res.append(ev_l)
        # end = time()
        # print(end-start)

    return enc_res


def c_resolve(enc_res: List[bytes],keys: PARAMS):
    res = [AES_dec(keys.kenc, e) for e in enc_res]
    return res


if __name__ == "__main__":
    from time import time
    """
    test case
    """
    # small database
    f_wid = "./data/enron_inverted0.csv"
    f_idw = "./data/enron_index0.csv"
    ws = ["trade", "buyer"]  # 13,14
    # ws = ['trade','buyer','juan','gas']
    n = 100
    k = 2

    """
    edb setup 
    """
    start = time()
    keys = PARAMS()
    edb = EDB(n, k)
    edb.setup(f_wid, f_idw,keys)
    end = time()
    print(f"edb setup: {end-start} s")

    """
    Complete search process
    """
    inds = search(ws, edb,keys)
    print(inds)

    """
    Each step of the search process
    """
    start = time()
    token = c_gen_token(ws,keys)
    end = time()
    print(f"gen token: {end-start} s")

    start = time()
    enc_res = s_search(token, edb)
    end = time()
    print(f"search: {end-start} s")

    start = time()
    res = c_resolve(enc_res,keys)
    end = time()
    print(f"dec to get res: {end-start} s")
    print(f"res:{res}")
