import pickle
from Crypto.Random import get_random_bytes
from typing import List
import struct
from Utils.cryptoUtils import prf, AES_enc, AES_dec
from Utils.pbcUtils import pbcUtil
from Utils.TSet import TSet, cal_size, genStag
from Utils.BF import BF, get_pos_set
from Utils.SHVE import SHVE
from Utils.fileUtils import read_index
from dataclasses import dataclass


@dataclass
class PARAMS:
    ks: bytes = get_random_bytes(16)
    kx: bytes = get_random_bytes(16)
    ki: bytes = get_random_bytes(16)
    kz: bytes = get_random_bytes(16)
    kt: bytes = None


pbc = pbcUtil()
shve = SHVE()


class EDB:
    def __init__(self, n: int, p: float, k: int) -> None:
        self.n = n
        self.p = p
        self.tset = TSet(n, k)
        self.xset = BF(n, p)

    def EDBSetup(self, fpath_wid: str, keys: PARAMS):
        T = dict()
        msk = shve.setup()

        dct_wid = read_index(fpath_wid)

        # Each keyword
        for w, ids in dct_wid.items():
            ke = prf(keys.ks, w)
            xtrap = pbc.prfToZr(keys.kx, w)
            # Each id under the keyword
            t = []
            for i in range(len(ids)):
                # TSet
                ind = ids[i]
                xind = pbc.prfToZr(keys.ki, ind)
                z = pbc.prfToZr(keys.kz, w + str(i))
                y = pbc.mul2Zr(xind, ~z)
                y = pbc.Zr2Bytes(y)
                e = AES_enc(ke, ind)
                element = struct.pack("H", len(y)) + y + e
                t.append(element)
                # XSet
                # TODO: Correctness testing
                # print(w,ind)
                xtag = pbc.gToPower2(xind, xtrap)
                self.xset.add(str(xtag))
            T[w] = t
        keys.kt = self.tset.setup(T)
        self.xset = shve.encBF(msk, self.xset)
        return msk


"""
Complete search process
"""


def search(msk: bytes, ws: List[str], edb: EDB, keys: PARAMS) -> List[int]:
    # Tset
    w1 = ws[0]
    ke = prf(keys.ks, w1)
    stag = genStag(keys.kt, w1)
    t = edb.tset.retrive(stag)

    # Xset
    end = []
    for i, item in enumerate(t):
        bf = BF(edb.n, edb.p)
        (l,) = struct.unpack("H", item[:2])
        y = item[2 : 2 + l]
        y = pbc.bytes2Zr(y)
        e = item[2 + l :]

        for j in range(1, len(ws)):
            z = pbc.prfToZr(keys.kz, w1 + str(i))
            xtrap = pbc.prfToZr(keys.kx, ws[j])
            xtoken = pbc.gToPower2(z, xtrap)
            bf.add(str(pbc.pow(xtoken, y)))

        res_s = shve.keyGenFromBF(msk, bf)
        if shve.query(edb.xset, res_s) == True:
            ind = AES_dec(ke, e)
            end.append(ind)

    return end


"""
every step
"""


def c_gen_stag(ws: List[str], keys: PARAMS):
    return genStag(keys.kt, ws[0])


def s_retrive_stag(tset: TSet, stag: bytes):
    return tset.retrive(stag)


def c_gen_xtoken(t_len: int, ws: List[str], keys: PARAMS):
    xtoken = [] * t_len
    w1 = ws[0]
    for i in range(t_len):
        xtoken_i = []
        for j in range(1, len(ws)):
            z = pbc.prfToZr(keys.kz, w1 + str(i))
            xtrap = pbc.prfToZr(keys.kx, ws[j])
            xtoken_ij = pbc.gToPower2(z, xtrap)
            xtoken_i.append(xtoken_ij)
        xtoken.append(xtoken_i)
    return xtoken


def s_gen_pos_set(xtoken, t, n: int, p: float):
    es_all = []
    bfs = []
    bf = BF(n, p)
    for i, item in enumerate(t):
        (l,) = struct.unpack("H", item[:2])
        y = item[2 : 2 + l]
        y = pbc.bytes2Zr(y)
        e = item[2 + l :]
        es_all.append(e)

        lst = []
        for xtoken_ij in xtoken[i]:
            lst.append(str(pbc.pow(xtoken_ij, y)))
        pos_set = get_pos_set(lst, bf.k, bf.m)
        bfs.append(pos_set)
    return es_all, bfs


def c_keygen_from_pos_set(msk, bfs):
    key_list = []
    for bf in bfs:
        key = shve.keyGenFromBFPos(msk, bf)
        key_list.append(key)
    return key_list


def s_get_es(xset, es_all, key_list):
    es = []
    for i, key in enumerate(key_list):
        if shve.query(xset, key) == True:
            es.append(es_all[i])
    return es


def c_decrypt_e(es: List[bytes], ws: List[str], keys: PARAMS):
    ke = prf(keys.ks, ws[0])
    res = [AES_dec(ke, e) for e in es]
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
    # p = 0.0001
    p = pow(10, -6)
    k = 2

    """
    edb setup 
    """
    start = time()
    keys = PARAMS()
    edb = EDB(n, p, k)
    msk = edb.EDBSetup(filename, keys)
    end = time()
    print(f"edb setup: {end-start} s")
    # tset_size = cal_size(edb.tset)
    # print(f"tset size(cal lenth): {tset_size/1024} KB")
    # tset_size = len(pickle.dumps(edb.tset))
    # print(f"tset size(dump)     : {tset_size/1024} KB")
    # xset_size = len(edb.xset) *32
    # print(f"xset size(cal lenth): {xset_size/1024} KB")
    # xset_size = len(pickle.dumps(edb.xset))
    # print(f"xset size(dump)     : {xset_size/1024} KB")

    """
    Complete search process
    """
    inds = search(msk, ws, edb, keys)
    print(inds)

    """
    Each step of the search process
    """
    start = time()
    stag = c_gen_stag(ws, keys)
    end = time()
    print(f"gen stag: {end-start} s")

    start = time()
    t = s_retrive_stag(edb.tset, stag)
    end = time()
    print(f"retrive stag: {end-start} s")

    start = time()
    xtoken = c_gen_xtoken(len(t), ws, keys)
    end = time()
    print(f"gen xtoken: {end-start} s")

    start = time()
    es_all, bfs = s_gen_pos_set(xtoken, t, edb.n, edb.p)
    end = time()
    print(f"gen bfs(pos set): {end-start} s")

    start = time()
    key_list = c_keygen_from_pos_set(msk, bfs)
    end = time()
    print(f"keygen form bf(pos set): {end-start} s")

    start = time()
    es = s_get_es(edb.xset, es_all, key_list)
    end = time()
    print(f"get enc res: {end-start} s")

    start = time()
    res = c_decrypt_e(es, ws, keys)
    end = time()
    print(f"dec to get res: {end-start} s")
    print(f"res:{res}")
