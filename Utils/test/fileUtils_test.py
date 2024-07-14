import init
from Utils.fileUtils import read_index

if __name__ == "__main__":
    dct = read_index("./data/wid.dat")
    print(dct)
    dct = read_index("./data/idw.dat")
    print(dct)
