import sys
from os import path

current_dir = path.dirname(path.abspath(__file__))
up_dir = path.abspath(path.dirname(current_dir))
up_up_dir = path.abspath(path.dirname(up_dir))

# Utils包的父目录的路径
sys.path.append(up_up_dir)
