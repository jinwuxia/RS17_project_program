import sys
import csv


def readCSV(fileName):
    resList = list()
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID, order, stype, callerName, calleeName, m1_para, m2_para, className1, className2, m1_return, m2_return, addweight] = each
            if traceID == 'traceID':
                continue
            resList.append([className1, className2, addweight])
    return resList

def writeCSV(fileName, alist):
    with open(fileName, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)
            
            
classdepList = readCSV(sys.argv[1])
writeCSV(sys.argv[2], classdepList)
