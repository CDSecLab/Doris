import init
from Utils.pbcUtils import *
from Crypto.Random import get_random_bytes


def pbc_test():
    pbc = pbcUtil()
    k1 = get_random_bytes(16)
    k2 = get_random_bytes(16)
    msg = get_random_bytes(4)
    # The message is mapped onto Zr by prf
    n = pbc.prfToZr(k1, str(msg))
    m = pbc.prfToZr(k2, str(msg))
    print(f"n:{n}\nm:{m}")
    g2p = pbc.gToPower(n)
    g2p2 = pbc.gToPower2(n, m)
    print(f"g2p:{g2p}\ng2p2:{g2p2}")

    # Element type conversion
    # Zr Element & bytes
    nbstr = pbc.Zr2Bytes(n)
    nEle = pbc.bytes2Zr(nbstr)
    assert nEle == n

    # G1 Element & str
    temp = Element.random(pairing, G1)  # 随机生成G1上的元素
    print(type(temp), temp)
    str_t = str(temp)  # Element->str
    res = Element(pairing, G1, value=str_t)  # str->Element
    print(type(res), res)


if __name__ == "__main__":
    pbc_test()
