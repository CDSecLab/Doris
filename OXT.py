from Crypto.Random import get_random_bytes
from typing import List
import struct
from Utils.cryptoUtils import prf, AES_enc, AES_dec
from Utils.pbcUtils import pbcUtil
from Utils.TSet import TSet, genStag, cal_size
from Utils.BF import BF
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


class EDB:
    def __init__(self, n: int, p: float, k: int) -> None:
        """
        n: (w,id) pair num
        p: False positive rate of BF
        k: Expansion factor of TSet
        """
        self.tset = TSet(n, k)
        self.xset = BF(n, p)

    def EDBSetup(self, fpath_wid: str, keys: PARAMS):
        T = dict()

        # read the inverted index
        dct_wid = read_index(fpath_wid)

        # every keyword - ids
        for w, ids in dct_wid.items():
            ke = prf(keys.ks, w)
            xtrap = pbc.prfToZr(keys.kx, w)
            # every id in ids
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
                xtag = pbc.gToPower2(xind, xtrap)
                self.xset.add(str(xtag))
            T[w] = t

        keys.kt = self.tset.setup(T)


"""
Complete search process
"""


def search(ws: List[str], edb: EDB, keys: PARAMS) -> List[int]:
    # Tset
    w1 = ws[0]
    ke = prf(keys.ks, w1)
    stag = genStag(keys.kt, w1)
    t = edb.tset.retrive(stag)

    # Xset
    end = []
    for i, item in enumerate(t):
        (l,) = struct.unpack("H", item[:2])
        y = item[2 : 2 + l]
        y = pbc.bytes2Zr(y)
        e = item[2 + l :]

        # Used to mark how many remaining keywords the corresponding id has
        flag = 0
        for j in range(1, len(ws)):
            z = pbc.prfToZr(keys.kz, w1 + str(i))
            xtrap = pbc.prfToZr(keys.kx, ws[j])
            xtoken = pbc.gToPower2(z, xtrap)
            if str(pbc.pow(xtoken, y)) in edb.xset:
                flag += 1
        if flag == len(ws) - 1:
            ind = AES_dec(ke, e)
            end.append(ind)
    return end


"""
Each step of the search process
"""


def c_gen_stag(ws: List[str], keys: PARAMS):
    return genStag(keys.kt, ws[0])


def s_retrive_stag(tset: TSet, stag: bytes):
    return tset.retrive(stag)


def c_gen_xtoken(t_len: int, ws: List[str], keys: PARAMS):
    xtoken = [] * t_len
    for i in range(t_len):
        xtoken_i = []
        w1 = ws[0]
        for j in range(1, len(ws)):
            z = pbc.prfToZr(keys.kz, w1 + str(i))
            xtrap = pbc.prfToZr(keys.kx, ws[j])
            xtoken_ij = pbc.gToPower2(z, xtrap)
            xtoken_i.append(xtoken_ij)
        xtoken.append(xtoken_i)
    return xtoken


def s_get_es(xtoken, xset: BF, t):
    es = []
    for i, item in enumerate(t):
        (l,) = struct.unpack("H", item[:2])
        y = item[2 : 2 + l]
        y = pbc.bytes2Zr(y)
        e = item[2 + l :]

        flag = 0
        xtoken_i = xtoken[i]
        length = len(xtoken_i)
        for j in range(length):
            if str(pbc.pow(xtoken_i[j], y)) in xset:
                flag += 1
        if flag == length:
            es.append(e)
    return es


def c_decrypt_e(es: List[bytes], ws: List[str], keys: PARAMS):
    ke = prf(keys.ks, ws[0])
    res = [AES_dec(ke, e) for e in es]
    return res


if __name__ == "__main__":
    from time import time
    import pickle

    """
    test case
    """
    # small database
    filename = "./data/enron_inverted0.csv"
    ws = ["trade", "buyer"]  # 13,14
    ws = ["trade", "buyer", "juan", "gas"]
    n = 100
    p = 0.0001
    k = 2

    """
    edb setup 
    """
    start = time()
    keys = PARAMS()
    edb = EDB(n, p, k)
    edb.EDBSetup(filename, keys)
    end = time()
    print(f"edb setup: {end-start} s")
    tset_size = cal_size(edb.tset)
    print(f"tset size(cal lenth): {tset_size/1024} KB")
    tset_size = len(pickle.dumps(edb.tset))
    print(f"tset size(dump)     : {tset_size/1024} KB")
    xset_size = len(edb.xset) // 8
    print(f"xset size(cal lenth): {xset_size/1024} KB")
    xset_size = len(pickle.dumps(edb.xset))
    print(f"xset size(dump)     : {xset_size/1024} KB")

    """
    Complete search process
    """
    inds = search(ws, edb, keys)
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
    es = s_get_es(xtoken, edb.xset, t)
    end = time()
    print(f"get enc res: {end-start} s")

    start = time()
    res = c_decrypt_e(es, ws, keys)
    end = time()
    print(f"dec to get res: {end-start} s")
    print(f"res:{res}")
