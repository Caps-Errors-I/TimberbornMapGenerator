# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 19:41:25 2021

@author: Caps-Errors
"""

import json

def printDict(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))

def writeValue(dictTree, path, value):
    if len(path) == 1:
        dictTree[path[0]] = value
    else:
        next = dictTree.get(path[0], {})
        then = writeValue(next, path[1:], value)
        dictTree[path[0]] = then
    
    return dictTree

def generateArrayStrings(terrainMap):
    heightMap = ""
    scalarMap = ""
    flowMap = ""
    
    for row in terrainMap:
        for element in row:
            heightMap = heightMap + element.astype(str) + " "
            scalarMap = scalarMap + "0 "
            flowMap = flowMap + "0:0:0:0 "
            
    heightMap = heightMap[0:-1]
    scalarMap = scalarMap[0:-1]
    flowMap = flowMap[0:-1]
    
    return heightMap, scalarMap, flowMap
    
def saveTerrainMap(map, x, y):
    heightMap, scalarMap, flowMap = generateArrayStrings(map)
    
    template = open ("Template.json", "r")
    templateString = template.read()
    template.close()
    
    mapJson = json.loads(templateString)
    mapJson = writeValue(mapJson, ["Singletons", "MapSize", "Size", "X"], x)
    mapJson = writeValue(mapJson, ["Singletons", "MapSize", "Size", "Y"], y)
    
    mapJson = writeValue(mapJson, ["Singletons", "TerrainMap", "Heights", "Array"], heightMap)
    mapJson = writeValue(mapJson, ["Singletons", "SoilMoistureSimulator", "MoistureLevels", "Array"], scalarMap)
    mapJson = writeValue(mapJson, ["Singletons", "WaterMap", "WaterDepths", "Array"], scalarMap)
    mapJson = writeValue(mapJson, ["Singletons", "WaterMap", "Outflows", "Array"], flowMap)
    
    output = open("maps/newMap.json", "w")
    output.write(json.dumps(mapJson))
    output.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
