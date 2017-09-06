import sys
import csv

def readCSV2Dict(fileName):
    methodDict = dict()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [componentID, methodName, returnType, paralist] = each
            if componentID == "component":
                continue
            else:
                if methodName not in methodDict:
                    methodDict[methodName] = 1
    return methodDict

def compareDict(dict1, dict2):
    notInDict2 = list()
    for key1 in dict1:
        if key1 not in dict2:
            notInDict2.append(key1)
    return notInDict2

#python compareCodeTraceCompAPI.py  codeAPI.csv   traceAPI.csv
if __name__ == "__main__":
    codeAPIName = sys.argv[1]
    traceAPIName = sys.argv[2]
    codeMethodDict = readCSV2Dict(codeAPIName)
    traceMethodDict = readCSV2Dict(traceAPIName)
    notInCodeList = compareDict(traceMethodDict, codeMethodDict)
    notInTraceList = compareDict(codeMethodDict, traceMethodDict)

    for each in notInTraceList:
        print each
    print "XXXXXX\n\n"
    for each in notInCodeList:
        print each
