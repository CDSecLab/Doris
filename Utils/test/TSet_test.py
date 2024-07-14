import init
from Utils import *
from time import time
import pickle

if __name__ == "__main__":
    T = {"a": [get_random_bytes(32) for _ in range(2)], "b": [b'sdf', b'zvcb']}

    count = 0
    for vs in T.values():
        count += len(vs)

    k = 2
    B = math.ceil(math.log2(count*k))
    S = math.ceil(math.log2(count*k))
    print(f"B:{B},S:{S}")

    start = time()
    tset = TSet(count, k)
    kt = tset.setup(T)
    # print(tset.t_set)
    end = time()
    print('gen tset', end-start, 's')

    stag = genStag(kt, 'b')

    start = time()
    t = tset.retrive(stag)
    print(t)
    end = time()
    print('retrive', end-start, 's')

    # cal size
    print(f'cal size: {cal_size(tset)}')
    print(f'pickle dumps: {len(pickle.dumps(tset))}')
