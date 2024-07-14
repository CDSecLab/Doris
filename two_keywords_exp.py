import OXT
import HXT
import ConjFilter_alter
import Doris_XF
from time import time
import pickle

from Utils.log import get_logger
logger = get_logger('./log/two_keywords_exp.log')


def cal_comm_cost(object):
    try:
        tmp = pickle.dumps(object)
        return len(tmp)
    except TypeError as e:
        # print(e)
        n = len(object)
        m = len(object[0])
        return n * m * 64


def oxt_test(n, p, k, fpath, w1_dct: dict, w2: str):
    keys = OXT.PARAMS()
    edb = OXT.EDB(n, p, k)
    edb.EDBSetup(fpath,keys)
    times = 10

    for w1, id_num in w1_dct.items():
        ws = [w1, w2]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            stag = OXT.c_gen_stag(ws,keys)
            end = time()
            gen_token_time.append(end - start)

            start = time()
            t = OXT.s_retrive_stag(edb.tset, stag)
            end = time()
            server_time.append(end - start)

            start = time()
            xtoken = OXT.c_gen_xtoken(len(t), ws,keys)
            end = time()
            gen_token_time[-1] += end - start

            start = time()
            es = OXT.s_get_es(xtoken, edb.xset, t)
            end = time()
            server_time[-1] += end - start

            # res = OXT.c_decrypt_e(es, ws,keys)
            # print(res)

        token_size = cal_comm_cost(xtoken) + cal_comm_cost(stag)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(f"OXT,{id_num},{gen_token_time:.6f},{token_size},{server_time:.6f}")


def hxt_test(n, p, k, fpath, w1_dct: dict, w2: str):
    keys = HXT.PARAMS()
    edb = HXT.EDB(n, p, k)
    msk = edb.EDBSetup(fpath,keys)
    times = 10

    for w1, id_num in w1_dct.items():
        ws = [w1, w2]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            stag = HXT.c_gen_stag(ws,keys)
            end = time()
            gen_token_time.append(end - start)

            start = time()
            t = HXT.s_retrive_stag(edb.tset, stag)
            end = time()
            server_time.append(end - start)

            start = time()
            xtoken = HXT.c_gen_xtoken(len(t), ws,keys)
            end = time()
            gen_token_time[-1] += end - start

            start = time()
            es_all, bfs = HXT.s_gen_pos_set(xtoken, t, edb.n, edb.p)
            end = time()
            server_time[-1] += end - start

            start = time()
            key_list = HXT.c_keygen_from_pos_set(msk, bfs)
            end = time()
            gen_token_time[-1] += end - start

            start = time()
            es = HXT.s_get_es(edb.xset, es_all, key_list)
            end = time()
            server_time[-1] += end - start

            # res = HXT.c_decrypt_e(es, ws,keys)
            # print(res)

        token_size = cal_comm_cost(keys) + cal_comm_cost(xtoken) + cal_comm_cost(stag)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(f"HXT,{id_num},{gen_token_time:.6f},{token_size},{server_time:.6f}")


def conjFilter_alter_test(n, k, fpath_wid, fpath_idw, w1_dct: dict, w2: str):
    keys = ConjFilter_alter.PARAMS()
    edb = ConjFilter_alter.EDB(n, k)
    edb.setup(fpath_wid, fpath_idw,keys)
    times = 10

    for w1, id_num in w1_dct.items():
        ws = [w1, w2]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            token = ConjFilter_alter.c_gen_token(ws,keys)
            end = time()
            gen_token_time.append(end - start)

            start = time()
            enc_res = ConjFilter_alter.s_search(token, edb)
            end = time()
            server_time.append(end - start)

            # res = ConjFilter_alter.c_resolve(enc_res,keys)
            # print(res)

        token_size = cal_comm_cost(token)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(
            f"ConjFilter,{id_num},{gen_token_time:.6f},{token_size},{server_time:.6f}"
        )


def hxt_xf_test(n, k, fpath_wid, fpath_idw, w1_dct: dict, w2: str):
    keys = Doris_XF.PARAMS()
    edb = Doris_XF.EDB(n, k)
    msk = edb.setup(fpath_wid, fpath_idw,keys)
    times = 10

    for w1, id_num in w1_dct.items():
        ws = [w1, w2]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            stag = Doris_XF.c_gen_stag(ws,keys)
            end = time()
            gen_token_time.append(end - start)

            server_time
            t = Doris_XF.s_retrive_stag(edb.tset, stag)
            end = time()
            server_time.append(end - start)

            start = time()
            xtoken = Doris_XF.c_gen_xtoken(msk, len(t), ws,keys)
            end = time()
            gen_token_time[-1] += end - start

            start = time()
            es = Doris_XF.s_get_es(xtoken, t, edb.ct)
            end = time()
            server_time[-1] += end - start

            # res = HXT_plus_XF.c_decrypt_e(es, ws,keys)
            # print(res)

        token_size = cal_comm_cost(xtoken) + cal_comm_cost(stag)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(
            f"HXT_XF,{id_num},{gen_token_time:.6f},{token_size},{server_time:.6f}"
        )


if __name__ == "__main__":
    """
    database
    """
    k = 2
    p = pow(10, -6)
    w2 = "auctions"
    
    # --------------------- big database(128GB RAM) -------------------------
    # n = pow(10, 6)
    # fpath_wid = "./data/enron_inverted4.csv"
    # fpath_idw = "./data/enron_index4.csv"
    # w1_dct = {
    #     "bluewxtitle": 10,
    #     "kupiecki": 101,
    #     "post": 200,
    #     "little": 500,
    #     "james": 999,
    #     "services": 1980,
    #     "market": 2878,
    #     "john": 3982,
    #     "energy": 5031,
    #     "subject": 5946,
    #     "gas": 6436,
    #     "sent": 7608,
    #     "thanks": 9148,
    #     "enron": 18146,
    # }

    # --------------------- small database -------------------------
    n = 28063
    fpath_wid = "./data/wid.csv"
    fpath_idw = "./data/idw.csv"
    w1_dct = {
        "bluewxtitle": 10,
        "kupiecki": 101,
        "post": 200,
        "little": 500,
        "james": 999,
        "services": 1980,
        "market": 2878,
        "john": 3982,
        "energy": 5031,
        "subject": 5946,
        "gas": 6436,
    }

    """
    exp
    """
    start = time()
    logger.info(f"protocol,id_num,gen_token_time,token_size,server_time")
    # OXT
    oxt_test(n, p, k, fpath_wid, w1_dct, w2)

    # HXT
    hxt_test(n, p, k, fpath_wid, w1_dct, w2)

    # ConjFilter
    conjFilter_alter_test(n, k, fpath_wid, fpath_idw, w1_dct, w2)

    # HXT_XF
    hxt_xf_test(n, k, fpath_wid, fpath_idw, w1_dct, w2)
    
    end = time()
    print(f"two keywords exp use time:{end-start}")