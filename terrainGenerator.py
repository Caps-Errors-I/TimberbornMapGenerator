# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:51:25 2021

@author: Caps-Errors
"""

import matplotlib.pyplot as plt
import numpy as np
import time as time

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
    # Array of all zeroes
    map = np.zeros((xSize, ySize))
    # Generate perlin maps of various size features and add them together
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

def generateSlopeMap(xSize, ySize, slope):
    # Generate a sloped gradient with height slope
    # This puts a bias on the map that improves layout later
    # This could be improved by putting in a directional gradient but linear is easy
    slopeMap = np.zeros((xSize, ySize))
    value = 0
    for x in range(xSize):
        value = slope / xSize * x
        for y in range(ySize):
            slopeMap[x,y] = value
    return slopeMap

def generateRiverSlopeMap(xSize, ySize, nodes, windiness=0.75, givenWidth=2, depth=0.2):
    # This generates a river with a number of nodes.
    # Windiness should be a float between 0.0 and 1.0, with 1.0 meaning the river
    #   will twist back and forth the whole width of the map.
    # Width and depth are integers for how wide and deep the path will be.

    # First, random phase angles (radians)
    angle1 = np.random.rand() * 2.0 * 3.14159
    angle2 = np.random.rand() * 2.0 * 3.14159
    angle3 = np.random.rand() * 2.0 * 3.14159

    riverMap = np.zeros((xSize, ySize))
    for x in np.arange(0.0,xSize,0.2):
        # Calculate center
        # Using three sin functions for additional meandering
        omega1 = ((x/xSize) * 2.0 * 3.14159 * nodes*0.4) + angle1
        omega2 = ((x/xSize) * 2.0 * 3.14159 * nodes*0.4) + angle2
        omega3 = ((x/xSize) * 2.0 * 3.14159 * nodes*0.4) + angle3
        center = 0.5 * np.sin(omega1*1) * (windiness) + \
                 0.3 * np.sin(omega2*3) * (windiness) + \
                 0.1 * np.sin(omega3*5) * (windiness)
        
        # This ranges from -1 to 1, draw on appropriate y center
        # I also want to hold this variable for a minute.
        center2 = int(center * ySize/2 + ySize/2)

        # Draw a bunch of circles. For each circle, evaluate a subset of tiles to see if
        # they are in the circle.
        
        # We're gonna tweak the size of the circle to add some wider parts to the bends
        # Maybe more realistic?

        width = givenWidth + givenWidth * 1.2 * abs(center)
        
        for x2 in range(max(int(x-width),0), min(int(x+width), xSize)):
            for y in range(max(int(center2-width),0), min(int(center2+width), ySize)):
                a = np.array((x, center2))
                b = np.array((x2, y))

                dist = np.linalg.norm(a-b)
                if (dist < width):
                    riverMap[x2,y] = 0-depth
        
    return riverMap


def main():
    x = 128
    y = 128
    
    # Generate the Perlin map
    # seed = 47
    seed = int(time.time() % (2**30-1))
    map = generateMultiLayerPerlin(x, y, seed)

#    This line used for debugging new layers with lots of zeroes
#    map = np.zeros((x, y))
    
    # Add the slope
    map = map + generateSlopeMap(x, y, 0.8)
    
    # There is probably some way to draw a river directly with plot libraries, 
    # but I am not smart enough to do so.
    map = map + generateRiverSlopeMap(x, y, 2)
    
    plt.imshow(map,origin='upper')

    plt.show()

    print(map.min())
    print(map.max())
    
    normalized = convert(map,1,16)
    
    print(normalized.min())
    print(normalized.max())
    
    saveTerrainMap(normalized, x, y)
    
if __name__ == "__main__":
    main()