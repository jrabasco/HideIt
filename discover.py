from PIL import Image
import numpy as np
import sys, os
from progress_bar import ProgressBar

def get_bit(pos, img):
    # avoids modifying thumbnail
    size = img.shape[0]*img.shape[1] - 4096
    rgb = pos//size
    if rgb > 2:
        raise IndexError("Position is too large")
    pos = pos % size + 4096
    x,y = pos // img.shape[1], pos % img.shape[1]
    return img[x][y][rgb] & 1


with Image.open(sys.argv[1]) as img:
    with open(sys.argv[2], "w+") as out:
        arrimg = np.array(img)
        pos = 0
        cur_char = ''
        size_str = ""
        while cur_char != "|":
            ord_chr = 0
            for i in range(8):
                bit = get_bit(pos, arrimg)
                pos += 1
                ord_chr = ord_chr | bit << i
            cur_char = chr(ord_chr)
            size_str += cur_char
        size = int(size_str[:-1])
        pb = ProgressBar(size)
        pb.begin()
        for i in range(size):
            ord_chr = 0
            for i in range(8):
                bit = get_bit(pos, arrimg)
                pos += 1
                ord_chr = ord_chr | bit << i
            out.write(chr(ord_chr))
            pb.add_progress()

