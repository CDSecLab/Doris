from Crypto.Random import get_random_bytes
from typing import List
from Utils.cryptoUtils import prf, AES_enc, AES_dec
from Utils.TSet import TSet, genStag
from Utils.SSPE_XF import SSPE_XF, MSK
from Utils.fileUtils import read_index
from dataclasses import dataclass


@dataclass
class PARAMS:
    ke: bytes = get_random_bytes(16)
    kx: bytes = get_random_bytes(16)
    kt: bytes = None

sspe = SSPE_XF()


class EDB:
    def __init__(self, n: int, k: int) -> None:
        self.tset = TSet(n, k)
        self.ct = None  # sspe

    def setup(self, fpath_wid: str, fpath_idw: str,keys:PARAMS) -> MSK:
        dct_wid = read_index(fpath_wid)
        dct_idw = read_index(fpath_idw)

        T = dict()
        xset = set() 

        # Each keyword
        for w, ids in dct_wid.items():
            t = []
            i = 1
            kw = prf(keys.ke, w)
            # Each id under the keyword
            for id in ids:
                e = AES_enc(kw, id)
                # The rest of the w under that id
                ws = dct_idw.get(id).copy()  # Copy to prevent the w from being deleted
                ws.remove(w)

                for w_tmp in ws:
                    # TODO: Correctness testing
                    # print(w,w_tmp,id)
                    xtag = prf(keys.kx, w + w_tmp + str(i))
                    xset.add(xtag)
                t.append(e)
                i += 1
            T[w] = t
        keys.kt = self.tset.setup(T)

        msk_bf = sspe.setup(len(xset))
        # TODO: Correctness testing
        # print(f"xset element number: {len(xset)}")
        sspe.enc(msk_bf, xset)
        self.ct = msk_bf.xf

        return msk_bf.msk


"""
Complete search process
"""


def search(msk: MSK, ws: List[str], edb: EDB,keys:PARAMS) -> List[int]:
    # Tset
    w1 = ws[0]
    ke = prf(keys.ke, w1)
    stag = genStag(keys.kt, w1)
    t = edb.tset.retrive(stag)

    # Xset
    end = []
    for i, e in enumerate(t):
        QSet = []
        for j in range(1, len(ws)):
            qtag = prf(keys.kx, w1 + ws[j] + str(i + 1))
            QSet.append(qtag)

        xtoken = sspe.keyGen(msk, QSet)
        if sspe.dec(xtoken, edb.ct) == True:
            ind = AES_dec(ke, e)
            end.append(ind)
    return end


"""
every step
"""


def c_gen_stag(ws: List[str],keys:PARAMS):
    return genStag(keys.kt, ws[0])


def s_retrive_stag(tset: TSet, stag: bytes):
    return tset.retrive(stag)


def c_gen_xtoken(msk: MSK, t_len: int, ws: List[str],keys:PARAMS):
    xtoken = []
    w1 = ws[0]
    for i in range(t_len):
        QSet = []
        for j in range(1, len(ws)):
            qtag = prf(keys.kx, w1 + ws[j] + str(i + 1))
            QSet.append(qtag)

        key = sspe.keyGen(msk, QSet)
        xtoken.append(key)
    return xtoken


def s_get_es(xtoken, t, ct) -> List[bytes]:
    es = []
    for i, e in enumerate(t):
        # start = time()
        s = xtoken[i]
        if sspe.dec(s, ct) == True:
            es.append(e)
        # end = time()
        # print(end-start)
    return es


def c_decrypt_e(es: List[bytes], ws: List[str],keys:PARAMS):
    ke = prf(keys.ke, ws[0])
    res = [AES_dec(ke, e) for e in es]
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
    ws = ["trade", "buyer", "juan", "gas"]
    n = 100
    k = 2

    """
    edb setup 
    """
    start = time()
    keys = PARAMS()
    edb = EDB(n, k)
    msk = edb.setup(f_wid, f_idw,keys)
    end = time()
    print(f"edb setup: {end-start} s")

    """
    Complete search process
    """
    inds = search(msk, ws, edb,keys)
    print(inds)

    """
    Each step of the search process
    """
    start = time()
    stag = c_gen_stag(ws,keys)
    end = time()
    print(f"gen stag: {end-start} s")

    start = time()
    t = s_retrive_stag(edb.tset, stag)
    end = time()
    print(f"retrive stag: {end-start} s")

    start = time()
    xtoken = c_gen_xtoken(msk, len(t), ws,keys)
    end = time()
    print(f"gen xtoken: {end-start} s")

    start = time()
    es = s_get_es(xtoken, t, edb.ct)
    end = time()
    print(f"get es: {end-start} s")

    start = time()
    res = c_decrypt_e(es, ws,keys)
    end = time()
    print(f"dec to get res: {end-start} s")
    print(f"res:{res}")
