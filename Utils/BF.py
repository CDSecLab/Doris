from bitarray import bitarray
import math
import mmh3


class BF(object):
    def __init__(self, n: int, p: float):
        m = optimalNumOfBits(n, p)
        k = optimalNumOfHash(n, m)

        # BF array
        self.bit_array = bitarray(m)
        self.bit_array.setall(0)
        # size
        self.m = m
        # hash_count
        self.k = k

    def __len__(self):
        return self.m

    def __iter__(self):
        return iter(self.bit_array)

    # add item to BF
    def add(self, item):
        for seed in range(self.k):
            index = mmh3.hash(item, seed) % self.m
            self.bit_array[index] = 1
        return self

    # add all items in set
    def add_all(self, items):
        for item in items:
            self.add(item)

    # Determine if the element is in BF
    def __contains__(self, item):
        out = True
        for seed in range(self.k):
            index = mmh3.hash(item, seed) % self.m
            if self.bit_array[index] == 0:
                out = False
        return out


def optimalNumOfBits(n: int, p: float) -> int:
    """
    Calculate BF array length

    n: The total number of elements expected to be inserted
    p: False positive rate
    Return: the size of BloomFilter m

    m = -{[n*ln(e)]/(ln2)^2}
    """
    return math.ceil(n * (-math.log(p)) / (math.log(2) * math.log(2)))


def optimalNumOfHash(n: int, m: int) -> int:
    """
    Calculate the number of hash functions k

    n: The total number of elements expected to be inserted
    m: the size of BloomFilter
    return the number of hash function k

    k = (m/n)*ln2
    """
    return math.ceil((m / n) * math.log(2))


def from_e_2_k(p: float) -> int:
    """
    Calculate the number of hash functions k
    The result of this function is same as optimalNumOfHash
    """
    k = math.ceil(-(math.log(p, 2)))
    return k


# Get positions of 1 (set)
def get_pos_set(items, hash_count: int, bf_size: int) -> set:
    pos_set = set()
    for item in items:
        for seed in range(hash_count):
            index = mmh3.hash(item, seed) % bf_size
            pos_set.add(index)
    return pos_set

# x Get positions of 1 (list)
def get_pos_list(items, hash_count: int, bf_size: int):
    index_set = []
    for item in items:
        for seed in range(hash_count):
            index = mmh3.hash(item, seed) % bf_size
            if index not in index_set:
                index_set.append(index)
    return index_set
