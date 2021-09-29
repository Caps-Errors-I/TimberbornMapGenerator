# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:51:25 2021

@author: Caps-Errors
"""

import numpy as np

# This code from stack overflow
def rawPerlin(x,y,seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi]+yi],xf,yf)
    n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = lerp(n00,n10,u)
    x2 = lerp(n01,n11,u)
    return lerp(x1,x2,v)

# This code from stack overflow
def lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

# This code from stack overflow
def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

# This code from stack overflow
def gradient(h,x,y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y

def generatePerlinMap(xSize, ySize, scale, amplitude, seedInput=0):
    linX = np.linspace(0,xSize/scale,xSize)
    linY = np.linspace(0,ySize/scale,ySize)
    
    x,y = np.meshgrid(linX,linY)
    
    map = rawPerlin(x,y,seed=seedInput)*amplitude
    
    return map
    