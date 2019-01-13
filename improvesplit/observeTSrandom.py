'''
randomly choose N% exectution traces, output the class coverage
'''

import sys
import csv
import random

GLOBAL_ORIGINAL_WORKFLOW = dict() #dict[traceID] = {className}
GLOBAL_CLASS_LIST = list()
#generate original traceIDlist with the specified TS number
#maxnumber is the number of original traceID
def randomChoose(maxnumber, traceCount):
    resultIDList = list()
    while len(resultIDList) < traceCount:
        index = random.randint(0, maxnumber - 1)
        if index not in resultIDList:
            resultIDList.append(index)
    resultIDList.sort()
    #print("choose trace: ", traceCount,  resultIDList)
    return resultIDList

#read original workflow files, store into GLOBAL_ORIGINAL_WORKFLOW
def readWorkflowCSV(fileName):
    global GLOBAL_ORIGINAL_WORKFLOW
    GLOBAL_ORIGINAL_WORKFLOW = dict()
    with open(fileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            traceID = each[0]
            #[traceID,order,structtype,method1,method2,m1_para,m2_para,className1,className2, m1_return, m2_return] = each
            class1 = each[7]
            class2 = each[8]
            if traceID == 'traceID':
                continue
            traceID = int(traceID)
            if traceID not in GLOBAL_ORIGINAL_WORKFLOW:
                GLOBAL_ORIGINAL_WORKFLOW[traceID] = set()
            GLOBAL_ORIGINAL_WORKFLOW[traceID].add(class1)
            GLOBAL_ORIGINAL_WORKFLOW[traceID].add(class2)
    return len(GLOBAL_ORIGINAL_WORKFLOW)




def readIncludeClass(fileName):
    global GLOBAL_CLASS_LIST
    GLOBAL_CLASS_LIST = list()
    with open(fileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            className = each[0]
            GLOBAL_CLASS_LIST.append(className)
    return len(GLOBAL_CLASS_LIST)


def getFinalCoverClass(selectedTraceIDList):
    coveredClassList = list()
    for traceId in selectedTraceIDList:
        for eachclass in GLOBAL_ORIGINAL_WORKFLOW[traceId]:
            if eachclass in GLOBAL_CLASS_LIST and  eachclass not in coveredClassList:
                coveredClassList.append(eachclass)
    return len(coveredClassList)

def writeCSV(fileName, alist):
    with open(fileName, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)

if __name__ == "__main__":
    workflowFile = sys.argv[1]
    classFile = sys.argv[2] #include class file

    #tsCountList = [14, 28, 42, 56] #solo
    #tsCountList = [17, 34, 51, 68] #roller
    #tsCountList = [22, 44, 66, 88] #agilefant
    #tsCountList = [553, 1106, 1659, 2212] #xwiki
    tsCountList = [7, 13, 20, 26] # springblog   33
    #tsCountList =[14, 28, 42, 56] #jforum    69

    allTraceCount = readWorkflowCSV(workflowFile)
    allClassCount = readIncludeClass(classFile)
    print("all trace:", allTraceCount)
    print("all class:", allClassCount)

    #traceName = ['_20percent', '_40percent', '_60percent', '_80percent']
    resultList = list()  #[]=eachtmp
    resultList.append(['20percent', '40percent', '60percent', '80percent'])
    for loop in range(0, 30):
        eachtmp = list() #[20% classpercent,  40% class percent, 60%, 80%]
        for index in range(0, len(tsCountList)):
            selectCount = tsCountList[index]
            selectedTraceIDList = randomChoose(allTraceCount, selectCount)
            coveredClassCount = getFinalCoverClass(selectedTraceIDList)
            percent = coveredClassCount / float(allClassCount)
            eachtmp.append(percent)
        resultList.append(eachtmp)

    #write the count to file
    print(resultList)
    writeCSV("randomStatis.csv", resultList)
