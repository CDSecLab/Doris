import math
import mmh3
from Crypto.Random import get_random_bytes
from collections import deque
import sys

byteorder = sys.byteorder

class XorFilter(object):
    def __init__(self, n: int):
        # size
        self.s = math.floor(1.23*n+32)
        self.l = self.s//3
        self.seed = 0  # Used to select r different hash functions
        # array
        # self.array = np.empty(self.s, dtype=bytes)
        self.array = [b'']*self.s

    def get_seed(self) -> int:
        return self.seed

    # Initialize the array and reselect r different hash functions
    def reset(self):
        self.seed += 3

    def _xor(self,a:bytes, b: bytes):
        int_a = int.from_bytes(a, byteorder)
        int_b = int.from_bytes(b, byteorder)
        int_enc = int_a ^ int_b
        return int_enc.to_bytes(32, byteorder)

    def __len__(self):
        return self.s

    def __iter__(self):
        return iter(self.array)

    def _hash_3(self, x):
        idxs = []
        for i in range(3):
            idx = (self.l*i)+(mmh3.hash(x, i+self.seed) % self.l)
            idxs.append(idx)
        return idxs

    def mapping_step(self, S):
        # init Auxiliary structure
        stack = []
        queue = deque()
        T = [[] for _ in range(self.s)]

        # hash to 3 different index
        for x in S:
            idxs = self._hash_3(x)
            for idx in idxs:
                T[idx].append(x)

        # Gets all positions with only one element
        for i, t in enumerate(T):
            if len(t) == 1:
                queue.append(i)

        # Loop to build stack
        while queue:
            i = queue.popleft()
            if not T[i]:
                continue
            x = T[i][0]
            stack.append((x, i))

            idxs = self._hash_3(x)
            for idx in idxs:
                T[idx].remove(x)
                if len(T[idx]) == 1:
                    queue.append(idx)

        if len(stack) != len(S):
            raise Exception("stack setup Failure")

        return stack

    def update(self, S):
        # A maximum of 5 mapping failures are allowed
        loop = 5
        for i in range(loop):
            try:
                stack = self.mapping_step(S)
                break
            except Exception as e:
                print(e)
                self.reset()

        for x, i in stack[::-1]:
            xor_res = format(x)
            idxs = self._hash_3(x)
            for idx in idxs:
                if idx != i:
                    if self.array[idx] == b'':
                        self.array[idx] = get_random_bytes(32)
                    xor_res = self._xor(xor_res, self.array[idx])
            self.array[i] = xor_res

        # fill with random
        for i in range(self.s):
            if self.array[i] == b'':
                self.array[i] = get_random_bytes(32)

    # XOR of 3 positions == hash(item)
    def __contains__(self, item):
        xor_res = format(item)
        idxs = self._hash_3(item)
        for idx in idxs:
            xor_res = self._xor(xor_res, self.array[idx])
        return (xor_res == bytes(32))


def format(item):
    # String type, autocomplete to 32-byte
    # convert to bytes
    if not (type(item) is bytes):
        item = str.zfill(item, 32)
        item = bytes(item, 'utf-8')
    return item

def get_pos(items,hash_count:int,xf_size:int,seed:int)->set:
    l = xf_size//hash_count
    pos_set = set()
    for item in items:
        for i in range(hash_count):
            idx = (l*i)+(mmh3.hash(item, i+seed) % l)
            if idx in pos_set:
                pos_set.remove(idx)
            else:
                pos_set.add(idx)
    return pos_set
