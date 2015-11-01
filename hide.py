from PIL import Image
import numpy as np
import sys, os
from progress_bar import ProgressBar

def set_px(pos, bit, img):
    # avoids modifying thumbnail
    size = img.shape[0]*img.shape[1] - 4096
    rgb = pos//size
    if rgb > 2:
        raise IndexError("Position is too large for image")
    n_pos = pos % size + 4096
    
    x,y = n_pos // img.shape[1], n_pos % img.shape[1]
    img[x][y][rgb] = img[x][y][rgb] & 254
    img[x][y][rgb] = img[x][y][rgb] | bit

with Image.open(sys.argv[1]) as img:
    with open(sys.argv[2], 'r') as input_txt:
        arrimg = np.array(img)
        pos = 0
        tasks = int(os.popen("wc -c " + sys.argv[2]).read().split(" ")[0])
        for c in str(tasks)+"|":
            for i in range(8):
                bit = (ord(c) & 1 << i) >> i
                set_px(pos, bit, arrimg)
                pos += 1
        pb = ProgressBar(tasks)
        pb.begin()
        for line in input_txt:
            for char in line:
                for i in range(8):
                    bit = (ord(char) & 1 << i) >> i
                    set_px(pos, bit, arrimg)
                    pos += 1
                pb.add_progress()

        output_img = Image.fromarray(arrimg)
        output_img.save(sys.argv[3])
