import init
from Utils.BF import *
from time import time
import test_case
from pympler import asizeof


def bf_params():
    ns = [pow(10,i) for i in range(8,9)]
    ps = [pow(10,-i) for i in range(3,7)]
    for p in ps:
        for n in ns:
            m = optimalNumOfBits(n, p)
            k = optimalNumOfHash(n, m)
            print(f"n:{n},p:{p}")
            print(f"m:{m}\nk:{k}\nm/n:{m//n}")


def basic_use_of_bf():
    '''
    Basic use of bloom filter
    - insert element
    - member test
    '''
    start = time()
    bf = BF(n, p)
    for data in database:
        bf.add(data)
    end = time()
    print(f"bf add all:{end-start} s")

    for data in database:
        assert data in bf
    assert "asdf" not in bf


def memory_test():
    '''
    bf memory test
    - Size of the Bloom filter itself
    - Size of the list of index that is 1 in the Bloom filter
    - Size of the set of index that is 1 in the Bloom filter
    '''
    bf = BF(n, p)
    print(f"n:{n}")

    start = time()
    bf.add_all(database)
    end = time()
    print(f"bf time:{end-start}")
    
    start = time()
    pos_list = get_pos_list(database, bf.k, bf.m)
    end = time()
    print(f"pos list time:{end-start}")
    
    start = time()
    pos_set = get_pos_set(database, bf.k, bf.m)
    end = time()
    print(f"pos set time:{end-start}")
    

    print(f"size of bit array: {asizeof.asizeof(bf.bit_array)}")
    print(f"size of index set: {asizeof.asizeof(pos_list)}")
    print(f"size of pos set: {asizeof.asizeof(pos_set)}")


if __name__ == "__main__":
    # parameter setting
    database = test_case.small_database
    n = len(database)
    p = 0.0001

    # test
    bf_params()

    basic_use_of_bf()

    memory_test()
