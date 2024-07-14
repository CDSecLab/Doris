import init
from Utils import *
from Crypto.Random import get_random_bytes
from random import sample
from time import time

if __name__ == "__main__":
    from random import sample
    from time import time

    # parameter setting
    # database = test_case.middle_database
    database = [get_random_bytes(32) for _ in range(10000)]
    n = len(database)

    sspe = SSPE_XF()
    msk_bf = sspe.setup(n)

    # enc universal set
    start = time()
    sspe.enc(msk_bf, database)
    ct = msk_bf.xf
    end = time()
    print(f"sspe enc:{end-start} s")

    sub_database = sample(database, len(database) - 4)

    # key gen from subset
    start = time()
    key = sspe.keyGen(msk_bf.msk, sub_database)
    end = time()
    print(f"key gen:{end-start} s")

    # query
    start = time()
    res = sspe.dec(key, ct)
    end = time()
    print(f"query:{end-start} s")
    assert res == True

    sub_database[0] = "****"
    key = sspe.keyGen(msk_bf.msk, sub_database)
    res = sspe.dec(key, ct)
    assert res == False
