import os

import numpy
import numpy as np
from PIL import Image
import sys

'''
    Testing for the Map Maker:
        we need some sprites to place in the map maker screen, so
        in order to do that while testing, this file can help us
        easily write some png images to test out:
            - write hollow box:
                writes a hollow box of a certain color
            - write solid box;
                writes a solid box of a certain color
'''

PATH = ''


def write_hollow_box(color=(255, 0, 0), name='hollow_box', border=10):
    arr = np.zeros((100, 100, 3), dtype=np.uint8)
    arr[:, 0:border] = color
    arr[:border, border:] = color
    arr[border:, -border:] = color
    arr[-border:, border:-border] = color
    img = Image.fromarray(arr)
    img.save(f'{PATH}/{name}.png')


def write_solid_box(color=(255, 255, 255), name='solid_box'):
    arr = np.zeros((100, 100, 3), dtype=np.uint8)

    for x in range(100):
        for y in range(100):
            arr[x, y, :] = list(color)
    print(np.shape(arr))
    img = Image.fromarray(arr)
    img.save(f'{PATH}/{name}.png')


PATH = 'tileset_default'

write_solid_box((255, 255, 255), name='white_solid')
write_solid_box((255, 0, 0), name='red_solid')
write_solid_box((0, 255, 0), name='green_solid')
