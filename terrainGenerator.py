# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:51:25 2021

@author: Caps-Errors
Contributions: Savanik
"""

import matplotlib.pyplot as plt
import numpy as np
import time as time
import uuid
import json

# Use uuid4() for random uuid's

from perlinMapgenerator import generatePerlinMap
from mapFileInterface import saveTerrainMap
from mapFileInterface import writeValue

def getTrees(map, targetTrees):
    # Just pine trees at the moment.
    # TODO: types of trees
    # TODO: maturity of trees scales with perlin height
    # TODO: Tree density

    xSize = len(map)
    ySize = len(map[0])

    #Place some clumps of trees!
    treeMap = np.zeros((xSize, ySize))
    treeNum = 0
    trees = []

    # Generate perlin map for noisy clusters
    seed = int(time.time() % (2**30-1))
    treeMap = generatePerlinMap(xSize, ySize, 16, 1.6, seed)
    
    maxH = treeMap.max()
    modifier = 1.00
    
    # Finding the right value for the number of trees we want
    while treeNum < targetTrees:
        treeNum = 0
        modifier -= 0.01
        prevalence = maxH * modifier
        for x in range(xSize):
            for y in range(ySize):
                if treeMap[x][y] > prevalence :
                    treeNum += 1

    treeNum = 0
    for x in range(xSize):
        for y in range(ySize):
            if treeMap[x][y] > prevalence :
                thisTree = dict()
                z = map[x][y]+1
                thisTree = writeValue(thisTree,["Id"],str(uuid.uuid4()))
                thisTree = writeValue(thisTree,["Template"],"Pine")
                thisTree = writeValue(thisTree,["Components","BlockObject","Coordinates","X"],int(x))
                thisTree = writeValue(thisTree,["Components","BlockObject","Coordinates","Y"],int(y))
                thisTree = writeValue(thisTree,["Components","BlockObject","Coordinates","Z"],int(z))
                thisTree = writeValue(thisTree,["Components","Growable","GrowthProgress"],float(1.0))
                thisTree = writeValue(thisTree,["Components","CoordinatesOffseter","CoordinatesOffset","X"],float(np.random.rand()-0.5))
                thisTree = writeValue(thisTree,["Components","CoordinatesOffseter","CoordinatesOffset","Y"],float(np.random.rand()-0.5))
                thisTree = writeValue(thisTree,["Components","NaturalResourceModelRandomizer","Rotation"],float(np.random.rand()*360))
                thisTree = writeValue(thisTree,["Components","NaturalResourceModelRandomizer","DiameterScale"],float(0.1*np.random.rand()+1.0))
                thisTree = writeValue(thisTree,["Components","NaturalResourceModelRandomizer","HeightScale"],float(0.1*np.random.rand()+1.0))
                thisTree = writeValue(thisTree,["Components","Yielder:Cuttable","Yield","Good","Id"],"Log")
                thisTree = writeValue(thisTree,["Components","Yielder:Cuttable","Yield", "Amount"],int(2))
                thisTree = writeValue(thisTree,["Components","GatherableYieldGrower","GrowthProgress"],float(np.random.rand()))
                trees.append(thisTree)
                #treeNum += 1
                #if treeNum < 5 : print(thisTree)
    #print(treeNum)
    
    return trees


def getRuins(map, targetRuins):
    xSize = len(map)
    ySize = len(map[0])

    #Place some clumps of ruins!
    ruinsMap = np.zeros((xSize, ySize))
    ruinsNum = 0
    ruins = []

    # Generate perlin map for noisy clusters
    seed = int(time.time() % (2**30-1))
    ruinsMap = generatePerlinMap(xSize, ySize, 16, 1.6, seed)
    
    maxH = ruinsMap.max()
    modifier = 1.00
    
    # Now to find the right value for the number of ruins we want
    while ruinsNum < targetRuins:
        ruinsNum = 0
        modifier -= 0.01
        prevalence = maxH * modifier
        for x in range(xSize):
            for y in range(ySize):
                if ruinsMap[x][y] > prevalence :
                    ruinsNum += 1

    for x in range(xSize):
        for y in range(ySize):
            if ruinsMap[x][y] > prevalence :
                thisRuin = dict()
                ruinHeight = int(max(min((ruinsMap[x][y]-prevalence)*400,8),1))
                ruinYield = int(ruinHeight * 15)
                variant = np.random.choice(['A','B','C','D','E'])
                z = map[x][y]+1
                thisRuin = writeValue(thisRuin,["Id"],str(uuid.uuid4()))
                thisRuin = writeValue(thisRuin,["Template"],"RuinColumnH" + str(ruinHeight))
                thisRuin = writeValue(thisRuin,["Components","BlockObject","Coordinates","X"],int(x))
                thisRuin = writeValue(thisRuin,["Components","BlockObject","Coordinates","Y"],int(y))
                thisRuin = writeValue(thisRuin,["Components","BlockObject","Coordinates","Z"],int(z))
                thisRuin = writeValue(thisRuin,["Components","Yielder:Ruin","Yield","Good","Id"],"ScrapMetal")
                thisRuin = writeValue(thisRuin,["Components","Yielder:Ruin","Yield","Amount",],int(ruinYield))
                thisRuin = writeValue(thisRuin,["Components","RuinModels","VariantId"],variant)
                thisRuin = writeValue(thisRuin,["Components","DryObject","IsDry"],bool(1))
                ruins.append(thisRuin)
    
    return ruins

def placeEntities(map, entities):
    #Placement and sanity check on entities

    entities.extend(getRuins(map,10))
    entities.extend(getTrees(map,800))
    #Water sources were placed earlier, but they need to exist at the proper height.
    # And we might as well sanity-check everything else, too.

    for this in entities:
        x = this["Components"]["BlockObject"]["Coordinates"]["X"]
        y = this["Components"]["BlockObject"]["Coordinates"]["Y"]
        z = this["Components"]["BlockObject"]["Coordinates"]["Z"]
        zMap = map[y][x]

        this["Components"]["BlockObject"]["Coordinates"]["Z"] = int(zMap)
    return entities

def convert(map, lower, upper):
    #Converts the map to a height lower-upper map.
    #Generally 1-16.
    
    min = map.min()
    zerod = map - min
    max = zerod.max()
    scaled = zerod * ((upper-lower)/max)
    mapped = scaled + lower
    result = mapped.astype(int)
    return result

def generateMultiLayerPerlin(xSize, ySize, seed, hills=1.0):
    # Makes a perlin map with height scaled by hills
    # Array of all zeroes
    map = np.zeros((xSize, ySize))
    # Generate perlin maps of various size features and add them together
#    map = map + generatePerlinMap(xSize, ySize, 128, 1.6, seed)
#    map = map + generatePerlinMap(xSize, ySize, 96, 1.2, seed)
#    map = map + generatePerlinMap(xSize, ySize, 64, 0.8, seed)
    map = map + generatePerlinMap(xSize, ySize, 48, 0.6 * hills, seed)
    map = map + generatePerlinMap(xSize, ySize, 32, 0.4 * hills, seed)
    map = map + generatePerlinMap(xSize, ySize, 24, 0.3 * hills, seed)
    map = map + generatePerlinMap(xSize, ySize, 16, 0.2 * hills, seed)
    map = map + generatePerlinMap(xSize, ySize, 12, 0.15 * hills, seed)
#    map = map + generatePerlinMap(xSize, ySize, 8, 0.1, seed)
    return map

def generateSlopeMap(xSize, ySize, slope):
    # Generate a sloped gradient with height slope
    # This puts a bias on the map that improves river layout later
    # This could be improved by putting in a vectored gradient but linear is easy to code
    slopeMap = np.zeros((xSize, ySize))
    value = 0
    for x in range(xSize):
        value = slope / xSize * x
        for y in range(ySize):
            slopeMap[x,y] = value
    return slopeMap

def generateRiverSlopeMap(map, entities, xSize, ySize, nodes, windiness=0.75, givenWidth=2, depth=0.2):
    # This generates a river as a complex sin function with a number of nodes.
    # Windiness should be a float between 0.0 and 1.0, with 1.0 meaning the river
    #   will twist back and forth the whole width of the map.
    # Width and depth are integers for how wide and deep the path will be.

    # First, random phase angles (radians)
    angle1 = np.random.rand() * 2.0 * 3.14159
    angle2 = np.random.rand() * 2.0 * 3.14159
    angle3 = np.random.rand() * 2.0 * 3.14159

    riverMap = np.zeros((xSize, ySize))

    #Placing edge water features.
    #Calculate our X center for our map edge.
    
    Y = ySize-1
    omega1 = ((Y/ySize) * 2.0 * 3.14159 * nodes*0.4) + angle1
    omega2 = ((Y/ySize) * 2.0 * 3.14159 * nodes*0.4) + angle2
    omega3 = ((Y/ySize) * 2.0 * 3.14159 * nodes*0.4) + angle3
    center = 0.5 * np.sin(omega1*1) * (windiness) + \
             0.3 * np.sin(omega2*3) * (windiness) + \
             0.1 * np.sin(omega3*5) * (windiness)
    center = int(center * ySize/2 + ySize/2)

    # We're going to guess on height and fix it later in normalization.

    minimum = map.min()
    height = map[Y][center]- depth - minimum
    maximum = map.max()
    Z = int(height * 16 / maximum)

    for x in range(-1,2): # This places 3 blocks
        riverSource = dict()
        riverSource = writeValue(riverSource,["Id"],str(uuid.uuid4()))
        riverSource = writeValue(riverSource,["Template"],"WaterSource")
        riverSource = writeValue(riverSource,["Components","WaterSource","SpecifiedStrength"],6.0)
        riverSource = writeValue(riverSource,["Components","WaterSource","CurrentStrength"],6.0)
        riverSource = writeValue(riverSource,["Components","BlockObject","Coordinates","X"],center+x)
        riverSource = writeValue(riverSource,["Components","BlockObject","Coordinates","Y"],Y)
        riverSource = writeValue(riverSource,["Components","BlockObject","Coordinates","Z"],Z)
        entities.append(riverSource)
    
    for x in np.arange(0.0,xSize,0.2):
        # Calculate center
        # Using three sin functions for additional meandering
        # They add together proportionally to come up to -1 to 1
        omega1 = ((x/ySize) * 2.0 * 3.14159 * nodes*0.4) + angle1
        omega2 = ((x/ySize) * 2.0 * 3.14159 * nodes*0.4) + angle2
        omega3 = ((x/ySize) * 2.0 * 3.14159 * nodes*0.4) + angle3
        center = 0.5 * np.sin(omega1*1) * (windiness) + \
                 0.3 * np.sin(omega2*3) * (windiness) + \
                 0.1 * np.sin(omega3*5) * (windiness)
        
        # Now we scale this to an appropriate y center
        # I also want to hold onto the regular variable for a minute.
        center2 = int(center * ySize/2 + ySize/2)

        # Draw a bunch of circles. For each circle, evaluate a subset of tiles to see if
        # they are in the circle.
        
        # We're gonna tweak the size of the circle to add some wider parts to the bends
        # Might look more realistic. Could add jitter later?

        width = givenWidth + givenWidth * 1.2 * abs(center)
        
        for x2 in range(max(int(x-width),0), min(int(x+width), xSize)):
            for y in range(max(int(center2-width),0), min(int(center2+width), ySize)):
                a = np.array((x, center2))
                b = np.array((x2, y))

                dist = np.linalg.norm(a-b)
                if (dist < width):
                    riverMap[x2,y] = 0-depth
    riverMap = map + riverMap
    return (riverMap, entities)

def slosh(heightMap, waterMap):
#Currently a stub. In theory, would model water movement.
    xSize = len(heightMap)
    ySize = len(heightMap[0])
    erosion = 0.001
    flowRate = 0.010
    totalWater = 0.0
    
    waterResultMap = np.zeros((xSize, ySize))
#    waterResultMap = waterMap.copy()
    heightResultMap = heightMap.copy()
    
    for i in range(0,xSize):
        for j in range(0,ySize):
            #If there is water
            if waterMap[i][j] > 0:
                #totalWater += waterMap[i][j]
                #If our water reached the edge of the map, it's going to flow off and take some soil with it.
                if ((i==0) or (i==xSize-1) or (j==0) or (j==ySize-1)):
                    if waterMap[i][j] < flowRate:
                        waterResultMap[i][j]=0
                    else:
                        waterResultMap[i][j]=waterMap[i][j]-flowRate
                    heightResultMap[i][j] -= erosion
                        
                else:
                    #find the lowest nearby point of water and land
                    height = heightMap[i][j]+waterMap[i][j]
                    lowest = height
                    v = [0, 0]
                    if heightMap[i-1][j-1]+waterMap[i-1][j-1] < lowest : v = [-1,-1]; lowest = heightMap[i-1][j-1]+waterMap[i-1][j-1]
                    if heightMap[i-1][j+0]+waterMap[i-1][j+0] < lowest : v = [-1,+0]; lowest = heightMap[i-1][j+0]+waterMap[i-1][j+0]
                    if heightMap[i-1][j+1]+waterMap[i-1][j+1] < lowest : v = [-1,+1]; lowest = heightMap[i-1][j+1]+waterMap[i-1][j+1]
                    if heightMap[i+0][j-1]+waterMap[i+0][j-1] < lowest : v = [+0,-1]; lowest = heightMap[i+0][j-1]+waterMap[i+0][j-1]
                    if heightMap[i+0][j+1]+waterMap[i+0][j+1] < lowest : v = [+0,+1]; lowest = heightMap[i+0][j+1]+waterMap[i+0][j+1]
                    if heightMap[i+1][j-1]+waterMap[i+1][j-1] < lowest : v = [+1,-1]; lowest = heightMap[i+1][j-1]+waterMap[i+1][j-1]
                    if heightMap[i+1][j+0]+waterMap[i+1][j+0] < lowest : v = [+1,+0]; lowest = heightMap[i+1][j+0]+waterMap[i+1][j+0]
                    if heightMap[i+1][j+1]+waterMap[i+1][j+1] < lowest : v = [+1,+1]; lowest = heightMap[i+1][j+1]+waterMap[i+1][j+1]
                    #water and a little bit of dirt go that way
                    if waterMap[i][j] < flowRate:
#                        waterResultMap[i][j]=0
                        waterResultMap[i+v[0]][j+v[1]] += waterMap[i][j]
                    else:
                        waterResultMap[i][j] = waterMap[i][j]-flowRate
                        waterResultMap[i+v[0]][j+v[1]] += flowRate
                    heightResultMap[i][j] -= erosion
                    heightResultMap[i+v[0]][j+v[1]] += erosion
#                    print("Moved ground from " + str(i) + "," + str(j) + " to " + str(i+v[0]) + "," + str(j+v[1]))
                    
                    #settling
                    if heightMap[i-1][j+0] < heightMap [i][j] :
                        heightResultMap[i][j] -= erosion
                        heightResultMap[i-1][j+0] += erosion
                    else :
                        heightResultMap[i][j] += erosion
                        heightResultMap[i-1][j+0] -= erosion

                    if heightMap[i+0][j-1] < heightMap [i][j] :
                        heightResultMap[i][j] -= erosion
                        heightResultMap[i+0][j-1] += erosion
                    else :
                        heightResultMap[i][j] += erosion
                        heightResultMap[i+0][j-1] -= erosion

                    if heightMap[i+0][j+1] < heightMap [i][j] :
                        heightResultMap[i][j] -= erosion
                        heightResultMap[i+0][j+1] += erosion
                    else :
                        heightResultMap[i][j] += erosion
                        heightResultMap[i+0][j+1] -= erosion

                    if heightMap[i+1][j+0] < heightMap [i][j] :
                        heightResultMap[i][j] -= erosion
                        heightResultMap[i+1][j+0] += erosion
                    else :
                        heightResultMap[i][j] += erosion
                        heightResultMap[i+1][j+0] -= erosion
                    
                    
    return (heightResultMap, waterResultMap)

def processWater(heightMap):
    # Currently a stub.
    
    # Adding water to the map and modelling erosion

    # We're going to run cellular simulation, dropping water at spots on the map and then
    # letting it flow around.
    
    # Assuming a well formed array
    
    xSize = len(heightMap)
    ySize = len(heightMap[0])
    
    waterDepth = np.zeros((xSize, ySize))
    waterDropSize = 0.01
    
    #Do we want a river?
    riverSource = 1
#    rX = int(np.random.rand() * xSize)
#    rY = int(np.random.rand() * ySize)
    rX = 32
    rY = 50
    riverAmount = 20
    
    #Do we want Rain?
    precipitation = 1
    rainAmount = 20
    
    #How many rounds of erosion shall we run?
    rounds = 400

    for i in range(0,rounds):
        if (i % 100) == 0 : print("Rounds: " + str(i) + " / " + str(rounds))
        if precipitation == 1 :
            # Make it rain
            for i in range(0,rainAmount):
                x = int(np.random.rand() * xSize)
                y = int(np.random.rand() * ySize)
                
                waterDepth[x][y] += waterDropSize
            
        if riverSource == 1 :
            # Add river water        
            waterDepth[rX][rY] += waterDropSize * riverAmount
        
        (heightMap, waterDepth) = slosh(heightMap,waterDepth)
   
    return heightMap


def main():
    x = 128
    y = 128
    tic = time.perf_counter()
    maptype = "River"
    map = np.zeros((x, y))
    entities = []

    if maptype == "River":
        # Start with a Perlin map
        #seed = 50
        seed = int(time.time() % (2**30-1))
        map = generateMultiLayerPerlin(x, y, seed, 0.5)

        toc = time.perf_counter()
        print("Time to Perlin: " + str(toc-tic))
        tic = time.perf_counter()
        
        # Add a biased slope
        map = map + generateSlopeMap(x, y, 0.8)
        
        toc = time.perf_counter()
        print("Time to Slope: " + str(toc-tic))
        tic = time.perf_counter()

        # There is probably some way to draw a river directly with plot libraries, 
        # but I am not smart enough to do so.
        # We are passing entities so we can have our water sources come back as well.

        (map, entities)= generateRiverSlopeMap(map, entities, x, y, 2)
        
        toc = time.perf_counter()
        print("Time to River: " + str(toc-tic))
        tic = time.perf_counter()

        # Modelling water flow!
        
        # I will need to review more physics papers before attempting hydrodynamic erosion.
        # Keeping the code around as a stub.
        
        #plt.imshow(map,origin='upper')
        #plt.show()
        #map = processWater(map)

    normalized = convert(map,1,16)
    entities = placeEntities(normalized,entities)
        
    saveTerrainMap(normalized, x, y, entities)
    
    toc = time.perf_counter()
    print("Time to save: " + str(toc-tic))
    
if __name__ == "__main__":
    main()