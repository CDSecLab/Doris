"""
ConjFilter original scheme
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
    kp: bytes = get_random_bytes(16)
    kx: bytes = get_random_bytes(16)
    kenc: bytes = get_random_bytes(16)
    msk: bytes = None


class EDB:
    def __init__(self, k: int) -> None:
        self.k = k
        self.EMM = None  # tset
        self.X = set()  # xset

    def _set_intersection(self, lst1, lst2):
        return set(lst1) & set(lst2)

    def setup(self, fpath_wid: str, keys: PARAMS):
        MM = dict()

        dct_wid = read_index(fpath_wid)

        count = 0  # Counts the number of elements to be inserted into the TSet
        for word_a, lst_a in dct_wid.items():
            for word_b, lst_b in dct_wid.items():
                if word_a == word_b:
                    continue

                vs = self._set_intersection(lst_a, lst_b)
                if not vs:
                    continue

                # TSet
                kt_a = prf(keys.kt, word_a)
                kenc_ab = prf(keys.kp, word_a + word_b)

                # XSet
                kx_ab = prf(keys.kx, word_a + word_b)

                t = []

                for v in vs:
                    # TSet
                    tag_av = prf(kt_a, v)
                    etag_av = AES_enc(kenc_ab, tag_av)
                    ev_v = AES_enc(keys.kenc, v)
                    element = struct.pack("H", len(etag_av)) + etag_av + ev_v
                    t.append(element)
                    # TODO: Correctness testing
                    # print(word_a,word_b,v)

                    # XSet
                    self.X.add(prf(kx_ab, tag_av))
                MM[word_a + word_b] = t
                count += len(t)
        # TODO: Correctness testing
        # print(f"xset element number: {len(self.X)}")

        self.EMM = TSet(count, self.k)
        keys.msk = self.EMM.setup(MM)


"""
Complete search process
"""


def search(ws: List[str], edb: EDB, keys: PARAMS) -> List[int]:
    # token
    stag = genStag(keys.msk, ws[0] + ws[1])
    kenc_12 = prf(keys.kp, ws[0] + ws[1])
    kxs = []
    for i in range(2, len(ws)):
        kx_i = prf(keys.kx, ws[0] + ws[i])
        kxs.append(kx_i)

    # tset&xset
    t = edb.EMM.retrive(stag)

    tag_lst = []
    ev_lst = []
    for i, item in enumerate(t):
        (l,) = struct.unpack("H", item[:2])
        etag_l = item[2 : 2 + l]
        ev_l = item[2 + l :]

        tag_l = AES_dec(kenc_12, etag_l)
        tag_lst.append(tag_l)
        ev_lst.append(ev_l)

    end = []
    for i in range(len(t)):
        for d in range(2, len(ws)):
            dtag_ld = prf(kxs[d - 2], tag_lst[i])
            if dtag_ld not in edb.X:
                break
        else:
            ind = AES_dec(keys.kenc, ev_lst[i])
            end.append(ind)
    return end


"""
every step
"""


@dataclass
class TOKEN:
    stag: bytes
    kenc_12: bytes
    kxs: List[bytes]


def c_gen_token(ws: List[str], keys: PARAMS) -> TOKEN:
    stag = genStag(keys.msk, ws[0] + ws[1])
    kenc_12 = prf(keys.kp, ws[0] + ws[1])
    kxs = []
    for i in range(2, len(ws)):
        kx_i = prf(keys.kx, ws[0] + ws[i])
        kxs.append(kx_i)
    return TOKEN(stag, kenc_12, kxs)


def s_search(token: TOKEN, edb: EDB, ws_len: int) -> List[bytes]:
    t = edb.EMM.retrive(token.stag)

    tag_lst = []
    ev_lst = []
    for i, item in enumerate(t):
        (l,) = struct.unpack("H", item[:2])
        etag_l = item[2 : 2 + l]
        ev_l = item[2 + l :]

        tag_l = AES_dec(token.kenc_12, etag_l)
        tag_lst.append(tag_l)
        ev_lst.append(ev_l)

    enc_res = []

    for i in range(len(t)):
        for d in range(2, ws_len):
            dtag_ld = prf(token.kxs[d - 2], tag_lst[i])
            if dtag_ld not in edb.X:
                break
        else:
            enc_res.append(ev_lst[i])
    return enc_res


def c_resolve(enc_res: List[bytes], keys: PARAMS):
    res = [AES_dec(keys.kenc, e) for e in enc_res]
    return res


if __name__ == "__main__":
    from time import time

    """
    test case
    """
    # small database
    filename = "./data/enron_inverted0.csv"
    ws = ["trade", "buyer"]  # 13,14
    ws = ["trade", "buyer", "juan", "gas"]
    n = 100
    k = 2

    """
    edb setup 
    """
    start = time()
    keys = PARAMS()
    edb = EDB(k)
    edb.setup(filename, keys)
    end = time()
    print(f"edb setup: {end-start} s")

    """
    Complete search process
    """
    inds = search(ws, edb, keys)
    print(inds)

    """
    Each step of the search process
    """
    start = time()
    token = c_gen_token(ws, keys)
    end = time()
    print(f"gen token: {end-start} s")

    start = time()
    enc_res = s_search(token, edb, len(ws))
    end = time()
    print(f"search: {end-start} s")

    start = time()
    res = c_resolve(enc_res, keys)
    end = time()
    print(f"dec to get res: {end-start} s")
    print(f"res:{res}")
