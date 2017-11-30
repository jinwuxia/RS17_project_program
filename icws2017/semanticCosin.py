import sys
import csv
import math

def readCSV(fileName):
    class2VectorDict = dict()#dict[0] = vector
    with open(fileName, 'r') as fp:
        reader = csv.reader(fp)
        for each in reader:
            print each
            className = each[0]
            del each[0]
            class2VectorDict[className] = [float(ele) for ele in each]
    return class2VectorDict

def cosin(v1, v2, n):
    fenzi = 0
    for i in range(0, n):
        fenzi += (v1[i] * v2[i])
    #fenmu
    v1_mo = 0
    v2_mo = 0
    for i in range(0, n):
        v1_mo += (v1[i] * v1[i])
        v2_mo += (v2[i] * v2[i])
    v1_mo = math.sqrt(v1_mo)
    v2_mo = math.sqrt(v2_mo)
    fenmu = v1_mo * v2_mo
    value = fenzi / float(fenmu)
    return value

def computeAllSim(class2VectorDict):
    listList = list()
    for class1 in class2VectorDict.keys():
        for class2 in class2VectorDict.keys():
            if class1 != class2:
                v1 = class2VectorDict[class1]
                v2 = class2VectorDict[class2]
                value = cosin(v1,v2, len(v1))
                listList.append([class1, class2, value])
    return listList

def writeCSV(listList, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print fileName

if __name__ == "__main__":
    semanticFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    class2VectorDict = readCSV(semanticFileName)
    listList = computeAllSim(class2VectorDict)
    writeCSV(listList, outputFileName)
