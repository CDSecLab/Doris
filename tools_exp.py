from Utils.SHVE import *
from Utils.SSPE_XF import *
from Utils.BF import *
from time import time
from random import sample
from Utils.fileUtils import *
import pickle

from Utils.log import get_logger
logger1 = get_logger('./log/tools_enc_exp.log')
logger2 = get_logger('./log/tools_query_exp.log')

"""
Testing the time consumption and storage of the encrypted set Y
n: |Y|
"""


def enc_test(n: int):
    database = set([get_random_bytes(8) for _ in range(n)])
    # print('gen random data done!')

    # SSPE_XF
    sspe = SSPE_XF()
    msk_bf = sspe.setup(n)

    start = time()
    sspe.enc(msk_bf, database)
    ct = msk_bf.xf
    end = time()
    ct_size = len(ct.array) * 32
    enc_time = end - start

    logger1.info(f"SSPE_XF,{n},{enc_time:.5f},{ct_size}")

    # SHVE
    hve = SHVE()
    msk = hve.setup()

    start = time()
    bf1 = BF(n, pow(10, -6))
    bf1.add_all(database)
    # print('bf done!')
    res_c = hve.encBF(msk, bf1)
    end = time()
    res_size = len(res_c) * 32
    enc_time = end - start

    logger1.info(f"SHVE,{n},{enc_time:.5f},{res_size}")


def cal_comm_cost(object):
    tmp = pickle.dumps(object)
    return len(tmp)


"""
对集合X生成查询token, 测试用时和存储
n: |Y|
m: |X|
"""


def keyGen_and_query_test(n: int, m_lst: List[int]):
    database = set([get_random_bytes(8) for _ in range(n)])

    # SSPE_XF
    sspe = SSPE_XF()
    msk_bf = sspe.setup(n)
    sspe.enc(msk_bf, database)
    ct = msk_bf.xf

    # SHVE
    hve = SHVE()
    msk = hve.setup()
    bf1 = BF(n, pow(10, -6))
    bf1.add_all(database)
    res_c = hve.encBF(msk, bf1)

    times = 5  # compute the average
    for m in m_lst:
        key_gen_time1 = 0
        key_size1 = 0
        query_time1 = 0

        key_gen_time3 = 0
        res_size3 = 0
        query_time3 = 0

        for _ in range(times):
            sub_database = sample(database, m)

            # SSPE_XF
            start = time()
            key = sspe.keyGen(msk_bf.msk, sub_database)
            end = time()
            key_size1 += cal_comm_cost(key)
            key_gen_time1 += end - start

            start = time()
            res = sspe.dec(key, ct)
            end = time()
            query_time1 += end - start
            assert res == True

            # SHVE_pos_set
            start = time()
            bf2 = BF(n, pow(10, -6))
            pos_set = get_pos_set(sub_database, bf2.k, bf2.m)
            res_pos = hve.keyGenFromBFPos(msk, pos_set)
            end = time()
            key_gen_time3 += end - start
            res_size3 += cal_comm_cost(res_pos)

            start = time()
            res = hve.query(res_c, res_pos)
            end = time()
            query_time3 += end - start
            assert res == True

        logger2.info(
            f"SSPE_XF,{n},{m},{key_gen_time1/times:.5f},{key_size1//times},{query_time1/times:.5f}"
        )
        logger2.info(
            f"SHVE_BF,{n},{m},{key_gen_time3/times:.5f},{res_size3//times},{query_time3/times:.5f}"
        )


if __name__ == "__main__":
    start = time()
    """
    enc_test
    """
    logger1.info("tool_name,n,enc_time,ct_size")
    # universal set: 10^2->10^6
    Y_size_lst = [pow(10, i) for i in range(2, 7)]
    for n in Y_size_lst:
        enc_test(n)

    """
    keygen_query_test
    """
    logger2.info("tool_name,n,m,key_gen_time,key_size,query_time")
    # subset: 1000-7000
    X_size_lst = [i * 1000 for i in range(1, 8)]
    keyGen_and_query_test(pow(10, 4), X_size_lst)

    end=time()
    print(f"tools exp use time:{end-start}")