import init
from Utils.cryptoUtils import prf, AES_dec, AES_enc
from Crypto.Random import get_random_bytes
from timeit import timeit


def prf_test():
    key = get_random_bytes(16)
    msg = b"asdf"
    t = timeit(lambda: prf(key, msg), number=times)
    print(f"prf:{t/times} s")


def hash_test():
    msg = b"asdf"
    t = timeit(lambda: hash(msg), number=times)
    print(f"hash:{t/times} s")


def aes_test():
    '''
    AES performance and consistency test
    '''
    key = get_random_bytes(16)
    msg = b"asdf"

    t = timeit(lambda: AES_enc(key, msg), number=times)
    print(f"AES enc:{t/times} s")

    c = AES_enc(key, msg)
    t = timeit(lambda: AES_dec(key, c), number=times)
    print(f"AES dec:{t/times} s")

    m_res = AES_dec(key, c)
    assert msg == m_res


if __name__ == "__main__":
    times = 1000  

    # test
    prf_test()

    hash_test()

    aes_test()
