import sys
import csv

def readCSV(fileName):
    classList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID,order,structtype,method1,method2,m1_para,\
               m2_para,className1,className2,m1_return,m2_return] = each
            if traceID == 'traceID':
                continue
            if className1 not in classList:
                classList.append(className1)
            if className2 not in classList:
                classList.append(className2)
    newClassList = list()
    for each in classList:
        newClassList.append([each])
    return newClassList

def writeCSV(fileName, classList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(classList)
    print fileName

#extract class from workflow.csv
if __name__ == '__main__':
    workflowFile = sys.argv[1]
    classFile = sys.argv[2]

    classList = readCSV(workflowFile)
    writeCSV(classFile, classList)
