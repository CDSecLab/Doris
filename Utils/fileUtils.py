# read index or inverted index
def read_index(fpath: str) -> dict:
    dct = {}  # w : [ids] or id : [ws]
    with open(fpath, 'r', encoding='utf-8') as fo:
        for line in fo:
            line = line.replace('\n', '')
            lst = line.split(",")

            key = lst.pop(0)
            values = lst

            for val in values:
                dct[key] = dct.get(key, []) + [val]
    return dct
