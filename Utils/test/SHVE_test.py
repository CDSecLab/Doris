import init
from Utils.SHVE import *
from Utils.BF import BF,get_pos_list,get_pos_set
import test_case
from time import time
from random import sample


def list_test():
    '''
    Whether querylist is a subset of wholelist
    '''
    hve = SHVE()
    msk = hve.setup()

    # key gen from subset
    start = time()
    res_s = hve.keyGenFromList(msk, querylist)
    end = time()
    print(f"key gen:{end-start} s")

    # enc universal set
    start = time()
    res_c = hve.encList(msk, wholelist_true)
    end = time()
    print(f"enc:{end-start} s")

    # query
    start = time()
    res = hve.query(res_c, res_s)
    end = time()
    print(f"query:{end-start} s")
    assert res == True

    res_c = hve.encList(msk, wholelist_false)
    res = hve.query(res_c, res_s)
    assert res == False


def bf_test():
    '''
    test with BF 
    Whether bf2 is a subset of bf1
    '''
    # prepare
    bf1 = BF(n, p)
    bf1.add_all(database)

    bf2 = BF(n, p)
    bf2.add_all(sub_database)

    index_set = get_pos_list(sub_database, bf2.k, bf2.m)
    pos_set = get_pos_set(sub_database, bf2.k, bf2.m)

    # setup
    hve = SHVE()
    msk = hve.setup()

    # enc universal set
    res_c = hve.encBF(msk, bf1)

    # key gen from subset
    res_index = hve.keyGenFromBFPos(msk, index_set)
    res_pos = hve.keyGenFromBFPos(msk, pos_set)
    res_bf = hve.keyGenFromBF(msk, bf2)

    # query
    assert hve.query(res_c, res_index) == True
    assert hve.query(res_c, res_pos) == True
    assert hve.query(res_c, res_bf) == True


if __name__ == '__main__':
    # list
    # - small
    querylist = [0, 1, 1, 0, 0, 0]
    wholelist_true = [1, 1, 1, 0, 0, 0]
    wholelist_false = [1, 0, 1, 0, 0, 0]

    # - middle
    # times = 100
    # querylist = querylist*times
    # wholelist_true = wholelist_true*times
    # wholelist_false = wholelist_true.copy()
    # wholelist_false[1] = 0

    list_test()

    # bf
    database = test_case.small_database
    sub_database = sample(database, len(database)-4)
    n = len(database)
    p: float = 0.0001

    bf_test()
