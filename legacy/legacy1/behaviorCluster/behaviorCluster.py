import sys
import csv


def readCSV(filename):
    oneDict = dict()
    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID, order, stype, m1, m2, m1_para, m2_para, class1, class2] = each
            if traceID not in oneDict:
                oneDict[traceID] = list()
            if class1 not in oneDict[traceID]:
                oneDict[traceID].append(class1)
            if class2 not in oneDict[traceID]:
                oneDict[traceID].append(class2)
    return oneDict


def output(oneDict):
    for traceID in oneDict:
        print traceID
        for  each in oneDict[traceID]:
            print each
        print "\n"

if __name__ == "__main__":
    filename = sys.argv[1]
    oneDict = readCSV(filename)
    output(oneDict)
            
            

