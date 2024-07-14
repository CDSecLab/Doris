import logging

def get_logger(name):
    logger = logging.getLogger(name)
    filename = f'{name}'
    fh = logging.FileHandler(filename, mode='w+', encoding='utf-8') # 输出到文件
    ch = logging.StreamHandler() # 输出到终端
    formatter = logging.Formatter('%(message)s')
    logger.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
