import OXT
import HXT
import ConjFilter_alter
import Doris_XF
from Utils.TSet import cal_size
from time import time


from Utils.log import get_logger

logger1 = get_logger("./log/setup_enron_exp.log")
logger2 = get_logger("./log/setup_enwiki_exp.log")


"""
single protocol test
"""


def oxt_test(n, p, k, fpath, db_name):
    keys = OXT.PARAMS()
    start = time()
    edb = OXT.EDB(n, p, k)
    edb.EDBSetup(fpath, keys)
    end = time()
    setup_time = end - start
    print(f"edb setup: {setup_time} s")

    tset_size = cal_size(edb.tset)
    xset_size = len(edb.xset) // 8

    if db_name == "enron":
        logger1.info(f"OXT,{n},{setup_time:.3f},{tset_size},{xset_size}")
    else:
        logger2.info(f"OXT,{n},{setup_time:.3f},{tset_size},{xset_size}")


def hxt_test(n, p, k, fpath, db_name):
    keys = HXT.PARAMS()
    start = time()
    edb = HXT.EDB(n, p, k)
    msk = edb.EDBSetup(fpath, keys)
    end = time()
    setup_time = end - start
    print(f"edb setup: {setup_time} s")

    tset_size = cal_size(edb.tset)
    xset_size = len(edb.xset) * 32

    if db_name == "enron":
        logger1.info(f"HXT,{n},{setup_time:.3f},{tset_size},{xset_size}")
    else:
        logger2.info(f"HXT,{n},{setup_time:.3f},{tset_size},{xset_size}")


def conjFilter_alter_test(n, k, fpath_wid, fpath_idw, db_name):
    keys = ConjFilter_alter.PARAMS()
    start = time()
    edb = ConjFilter_alter.EDB(n, k)
    edb.setup(fpath_wid, fpath_idw, keys)
    end = time()
    setup_time = end - start
    print(f"edb setup: {setup_time} s")

    tset_size = cal_size(edb.EMM)
    xset_size = len(edb.X) * 32

    if db_name == "enron":
        logger1.info(f"ConjFilter,{n},{setup_time:.3f},{tset_size},{xset_size}")
    else:
        logger2.info(f"ConjFilter,{n},{setup_time:.3f},{tset_size},{xset_size}")


def Doris_xf_test(n, k, fpath_wid, fpath_idw, db_name):
    keys = Doris_XF.PARAMS()
    start = time()
    edb = Doris_XF.EDB(n, k)
    msk = edb.setup(fpath_wid, fpath_idw, keys)
    end = time()
    setup_time = end - start
    print(f"edb setup: {setup_time} s")

    tset_size = cal_size(edb.tset)
    xset_size = len(edb.ct) * 32

    if db_name == "enron":
        logger1.info(f"Doris,{n},{setup_time:.3f},{tset_size},{xset_size}")
    else:
        logger2.info(f"Doris,{n},{setup_time:.3f},{tset_size},{xset_size}")


"""
test with two database
"""


def oxt_enron_enwiki():
    p = pow(10, -6)
    k = 2
    fpre = "./data/enron_inverted"
    ns = [100, 1000, 10000, 100000, 1000000]

    db_name = "enron"
    for i in range(cnt):
        fpath = fpre + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        oxt_test(n, p, k, fpath, db_name)

    fpre = "./data/enwiki_inverted"
    db_name = "enwiki"
    for i in range(cnt):
        fpath = fpre + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        oxt_test(n, p, k, fpath, db_name)


def hxt_enron_enwiki():
    p = pow(10, -6)
    k = 2
    fpre = "./data/enron_inverted"
    ns = [100, 1000, 10000, 100000, 1000000]

    db_name = "enron"
    for i in range(cnt):
        fpath = fpre + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        hxt_test(n, p, k, fpath, db_name)

    fpre = "./data/enwiki_inverted"
    db_name = "enwiki"
    for i in range(cnt):
        fpath = fpre + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        hxt_test(n, p, k, fpath, db_name)


def conjFilter_alter_enron_enwiki():
    k = 2
    fpre_wid = "./data/enron_inverted"
    fpre_idw = "./data/enron_index"
    ns = [100, 1000, 10000, 100000, 1000000]

    db_name = "enron"
    for i in range(cnt):
        fpath_wid = fpre_wid + str(i) + ".csv"
        fpath_idw = fpre_idw + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        conjFilter_alter_test(n, k, fpath_wid, fpath_idw, db_name)

    fpre_wid = "./data/enwiki_inverted"
    fpre_idw = "./data/enwiki_index"

    db_name = "enwiki"
    for i in range(cnt):
        fpath_wid = fpre_wid + str(i) + ".csv"
        fpath_idw = fpre_idw + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        conjFilter_alter_test(n, k, fpath_wid, fpath_idw, db_name)


def Doris_xf_enron_enwiki():
    k = 2
    ns = [100, 1000, 10000, 100000, 1000000]

    fpre_wid = "./data/enron_inverted"
    fpre_idw = "./data/enron_index"

    db_name = "enron"
    for i in range(cnt):
        fpath_wid = fpre_wid + str(i) + ".csv"
        fpath_idw = fpre_idw + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        Doris_xf_test(n, k, fpath_wid, fpath_idw, db_name)

    fpre_wid = "./data/enwiki_inverted"
    fpre_idw = "./data/enwiki_index"

    db_name = "enwiki"
    for i in range(cnt):
        fpath_wid = fpre_wid + str(i) + ".csv"
        fpath_idw = fpre_idw + str(i) + ".csv"
        n = ns[i]
        print("-" * 100)
        print(f"n: {n}")
        Doris_xf_test(n, k, fpath_wid, fpath_idw, db_name)


if __name__ == "__main__":
    logger1.info(f"protocol,pair_num,setup_time(s),tset_size(B),xset_size(B)")
    logger2.info(f"protocol,pair_num,setup_time(s),tset_size(B),xset_size(B)")

    """
    key/value pairs = [100, 1000, 10000, 100000, 1000000]
    Test the first 'cnt' database
    """
    cnt = 4

    start = time()
    # OXT
    oxt_enron_enwiki()

    # HXT
    hxt_enron_enwiki()

    # ConjFilter
    conjFilter_alter_enron_enwiki()

    # HXT_XF
    Doris_xf_enron_enwiki()

    end = time()
    print(f"setup exp use time:{end-start}")
