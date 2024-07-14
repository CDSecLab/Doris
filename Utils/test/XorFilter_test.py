import init
from Utils.XorFilter import XorFilter, get_pos
from time import time
from Crypto.Random import get_random_bytes


def basic_use(num: int):
    xfilter = XorFilter(num)
    S = set([get_random_bytes(32) for _ in range(num)])
    start = time()
    xfilter.update(S)
    end = time()
    print(f"time: {end-start}")
    # for s in S:
    #     assert s in xfilter


if __name__ == "__main__":
    nums = [pow(10, i) for i in range(1, 7)]
    for num in nums:
        basic_use(num)
