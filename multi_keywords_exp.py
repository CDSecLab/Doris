import OXT
import HXT
import ConjFilter_alter
import Doris_XF
from time import time
import pickle

from Utils.log import get_logger

logger = get_logger("./log/multi_keywords_exp.log")


def cal_comm_cost(object):
    try:
        tmp = pickle.dumps(object)
        return len(tmp)
    except TypeError as e:
        # print(e)
        n = len(object)
        m = len(object[0])
        return n * m * 64


def oxt_test(n, p, k, fpath, w_lst: list):
    keys = OXT.PARAMS()
    edb = OXT.EDB(n, p, k)
    edb.EDBSetup(fpath, keys)
    times = 10

    for q in range(2, len(w_lst) + 1, 2):
        ws = w_lst[:q]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            stag = OXT.c_gen_stag(ws, keys)
            end = time()
            gen_token_time.append(end - start)

            start = time()
            t = OXT.s_retrive_stag(edb.tset, stag)
            end = time()
            server_time.append(end - start)

            start = time()
            xtoken = OXT.c_gen_xtoken(len(t), ws, keys)
            end = time()
            gen_token_time[-1] += end - start

            start = time()
            es = OXT.s_get_es(xtoken, edb.xset, t)
            end = time()
            server_time[-1] += end - start

            # res = OXT.c_decrypt_e(es, ws,keys)
            # print(ws,res)

        token_size = cal_comm_cost(xtoken) + cal_comm_cost(stag)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(f"OXT,{q},{gen_token_time:.6f},{token_size},{server_time:.6f}")


def hxt_test_pos_set(n, p, k, fpath, w_lst: list):
    keys = HXT.PARAMS()
    edb = HXT.EDB(n, p, k)
    msk = edb.EDBSetup(fpath, keys)
    times = 10

    for q in range(2, len(w_lst) + 1, 2):
        ws = w_lst[:q]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            stag = HXT.c_gen_stag(ws, keys)
            end = time()
            gen_token_time.append(end - start)

            start = time()
            t = HXT.s_retrive_stag(edb.tset, stag)
            end = time()
            server_time.append(end - start)

            start = time()
            xtoken = HXT.c_gen_xtoken(len(t), ws, keys)
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
            # print(ws,res)

        token_size = cal_comm_cost(keys) + cal_comm_cost(xtoken) + cal_comm_cost(stag)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(f"HXT,{q},{gen_token_time:.6f},{token_size},{server_time:.6f}")


def conjFilter_alter_test(n, k, fpath_wid, fpath_idw, w_lst: list):
    keys = ConjFilter_alter.PARAMS()
    edb = ConjFilter_alter.EDB(n, k)
    edb.setup(fpath_wid, fpath_idw, keys)
    times = 10

    for q in range(2, len(w_lst) + 1, 2):
        ws = w_lst[:q]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            token = ConjFilter_alter.c_gen_token(ws, keys)
            end = time()
            gen_token_time.append(end - start)

            start = time()
            enc_res = ConjFilter_alter.s_search(token, edb)
            end = time()
            server_time.append(end - start)

            # res = ConjFilter_alter.c_resolve(enc_res,keys,keys)
            # print(ws,res)

        token_size = cal_comm_cost(token)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(
            f"ConjFilter,{q},{gen_token_time:.6f},{token_size},{server_time:.6f}"
        )


def hxt_xf_test(n, k, fpath_wid, fpath_idw, w_lst: list):
    keys = Doris_XF.PARAMS()
    edb = Doris_XF.EDB(n, k)
    msk = edb.setup(fpath_wid, fpath_idw, keys)
    times = 10

    for q in range(2, len(w_lst) + 1, 2):
        ws = w_lst[:q]
        gen_token_time = []
        server_time = []

        for _ in range(times):
            start = time()
            stag = Doris_XF.c_gen_stag(ws, keys)
            end = time()
            gen_token_time.append(end - start)

            server_time
            t = Doris_XF.s_retrive_stag(edb.tset, stag)
            end = time()
            server_time.append(end - start)

            start = time()
            xtoken = Doris_XF.c_gen_xtoken(msk, len(t), ws, keys)
            end = time()
            gen_token_time[-1] += end - start

            start = time()
            es = Doris_XF.s_get_es(xtoken, t, edb.ct)
            end = time()
            server_time[-1] += end - start

            # res = HXT_plus_XF.c_decrypt_e(es, ws,keys)
            # print(ws,res)

        token_size = cal_comm_cost(xtoken) + cal_comm_cost(stag)
        gen_token_time = (sum(gen_token_time) - max(gen_token_time)) / (times - 1)
        server_time = (sum(server_time) - max(server_time)) / (times - 1)

        logger.info(f"HXT_XF,{q},{gen_token_time:.6f},{token_size},{server_time:.6f}")


if __name__ == "__main__":
    """
    database
    """
    k = 2
    p = pow(10, -6)

    # --------------------- big database(128GB RAM) -------------------------
    # n = pow(10, 6)
    # fpath_wid = "./data/enron_inverted4.csv"
    # fpath_idw = "./data/enron_index4.csv"
    # # |DB('market')|: 2878
    # # |DB('thanks')|: 9148
    # ws_lst = ['thanks', 'order', 'market', 'prices', 'online',
    #           'level', 'access', 'customers', 'news', 'city', 'number']

    # --------------------- small database -------------------------
    n = 28063
    fpath_wid = "./data/wid.csv"
    fpath_idw = "./data/idw.csv"
    # |DB('market')|: 2878
    ws_lst = [
        "market",
        "order",
        "market",
        "prices",
        "online",
        "level",
        "access",
        "customers",
        "news",
        "city",
        "number",
    ]

    """
    exp
    """
    start = time()
    logger.info(f"protocol,q_num,gen_token_time(s),token_size(B),server_time(s)")
    # OXT
    oxt_test(n, p, k, fpath_wid, ws_lst)

    # HXT
    hxt_test_pos_set(n, p, k, fpath_wid, ws_lst)

    # ConjFilter
    conjFilter_alter_test(n, k, fpath_wid, fpath_idw, ws_lst)

    # HXT_XF
    hxt_xf_test(n, k, fpath_wid, fpath_idw, ws_lst)

    end = time()
    print(f"multi keywords exp use time:{end-start} s")
