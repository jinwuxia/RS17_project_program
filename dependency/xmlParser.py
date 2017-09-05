'''
extract class-class struct dependency from xmlFileName
xml file is exported from understand tool
'''

import sys
import csv
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET


class Node:
    def __init__(self, nodeID, shortname, longname):
        self.nodeID = nodeID
        self.shortname = shortname
        self.longname = longname

class Edge:
    def __init__(self, startNodeID, endNodeID, deps):
        self.startNodeID = startNodeID
        self.endNodeID = endNodeID
        self.deps = deps

#Extend,Typed,Import,Call,Cast,Create,Implement,Set,Use,Throw
class Depend:
    def __init__(self):
        self.Extend = 0
        self.Typed = 1
        self.Import = 2
        self.Call = 3
        self.Cast = 4
        self.Create = 5
        self.Implement = 6
        self.Set = 7
        self.Use = 8
        self.Throw = 9

NODEDict = dict()
EDGEList = list()
DEPEND = Depend()

def getDepList(deps):
    depsList = deps.split(', ')
    print depsList
    resList = ['0'] * 10
    for dep in depsList:
        if dep == 'Extend':
            resList[DEPEND.Extend] = '1'
        elif dep == 'Typed':
            resList[DEPEND.Typed] = '1'
        elif dep == 'Import':
            resList[DEPEND.Import] = '1'
        elif dep == 'Call':
            resList[DEPEND.Call] = '1'
        elif dep == 'Cast':
            resList[DEPEND.Cast] = '1'
        elif dep == 'Create':
            resList[DEPEND.Create] = '1'
        elif dep == 'Implement':
            resList[DEPEND.Implement] = '1'
        elif dep == 'Set':
            resList[DEPEND.Set] = '1'
        elif dep == 'Use':
            resList[DEPEND.Use] = '1'
        elif dep == 'Throw':
            resList[DEPEND.Throw] = '1'
        else:
            print "[ERROR] not found this type: ", dep
    return resList

def xmlParser(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    for node in root.findall('{http://www.cs.rpi.edu/XGMML}node'):
        nodeID = node.attrib['id']
        shortname = node[2].attrib['value'] #shortname
        longname = node[3].attrib['value'] #longname
        oneNode = Node(nodeID, shortname, longname)
        NODEDict[nodeID] = oneNode
        print nodeID, longname

    for edge in root.findall('{http://www.cs.rpi.edu/XGMML}edge'):
        startNodeID = edge.attrib['source']
        endNodeID = edge.attrib['target']
        deps = edge[4].attrib['value']   #deps
        depList = getDepList(deps)
        depStr = ''.join(depList)
        oneEdge = Edge(startNodeID, endNodeID, depStr)
        EDGEList.append(oneEdge)
        print startNodeID, endNodeID, depStr

def writeCSV(fileName):
    resList = list()
    for edge in EDGEList:
        startNodeLongname = NODEDict[edge.startNodeID].longname
        endNodeLongName = NODEDict[edge.endNodeID].longname
        deps = edge.deps
        resList.append([startNodeLongname, endNodeLongName, deps])

    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    print fileName

#python pro.py    jforum.xml   jforumxml.csv
if __name__ == '__main__':
    xmlFileName = sys.argv[1]
    csvFileName = sys.argv[2]
    #generate NODEDict, EDGEList
    xmlParser(xmlFileName)
    writeCSV(csvFileName)
