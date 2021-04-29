from particles import Particle
import matplotlib.pyplot as plt
import colorsys
from PIL import Image, ImageOps
import numpy as np

def colorcalc(self, h, s, v):
    raw_colors = colorsys.hsv_to_rgb(h, s, v)
    color = [round(color * 255) for color in raw_colors]
    return color


def draw_image():
    p1.engine()
    p2.engine()
    p3.engine()
    frame = p1.blurred_matrix + p2.blurred_matrix + p3.blurred_matrix
    frame = frame/np.max(frame)
    im = Image.fromarray(frame*256).convert("L")
    im = im.resize((8,8), resample=Image.NEAREST)
    im = ImageOps.colorize(im, black="black", mid="#04009a", white="#c0fefc")
    im.show()
    colorlist = list(im.getdata())
    showlist = [list(rgb) for rgb in colorlist]

    ##For debugging purposes
    # mat_lowres = np.array(im)
    # plt.matshow(mat_lowres)
    # plt.show(block=False)
    # plt.pause(1)
    # plt.close()
    return showlist

p1 = Particle()
p2 = Particle()
p3 = Particle()


for i in range(10):
    frame = draw_image()


