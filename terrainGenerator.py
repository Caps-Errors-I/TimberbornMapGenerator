# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:51:25 2021

@author: Caps-Errors
"""

import matplotlib.pyplot as plt
import numpy as np

from perlinMapgenerator import generatePerlinMap
from mapFileInterface import saveTerrainMap

def convert(map, lower, upper):
    min = map.min()
    zerod = map - min
    max = zerod.max()
    scaled = zerod * ((upper-lower)/max)
    mapped = scaled + lower
    result = mapped.astype(int)
    return result

def generateMultiLayerPerlin(xSize, ySize, seed):
    map = np.zeros((xSize, ySize))
#    map = map + generatePerlinMap(xSize, ySize, 128, 1.6, seed)
#    map = map + generatePerlinMap(xSize, ySize, 96, 1.2, seed)
#    map = map + generatePerlinMap(xSize, ySize, 64, 0.8, seed)
    map = map + generatePerlinMap(xSize, ySize, 48, 0.6, seed)
    map = map + generatePerlinMap(xSize, ySize, 32, 0.4, seed)
    map = map + generatePerlinMap(xSize, ySize, 24, 0.3, seed)
    map = map + generatePerlinMap(xSize, ySize, 16, 0.2, seed)
    map = map + generatePerlinMap(xSize, ySize, 12, 0.15, seed)
#    map = map + generatePerlinMap(xSize, ySize, 8, 0.1, seed)
    return map

def main():
    x = 128
    y = 128
    
    map = generateMultiLayerPerlin(x, y, 47)
    
    plt.imshow(map,origin='upper')
    
    print(map.min())
    print(map.max())
    
    normalized = convert(map,1,16)
    
    print(normalized.min())
    print(normalized.max())
    
    saveTerrainMap(normalized, x, y)
    
if __name__ == "__main__":
    main()