import sys
import csv
import random

GLOBAL_ORIGINAL_WORKFLOW = dict() #dict[traceID] = [[],]

#generate original traceIDlist with the specified TS number
#maxnumber is the number of original traceID
def randomChoose(maxnumber, traceCount):
    resultIDList = list()
    while len(resultIDList) < traceCount:
        index = random.randint(0, maxnumber - 1)
        if index not in resultIDList:
            resultIDList.append(index)
    resultIDList.sort()
    print("choose trace: ", traceCount,  resultIDList)
    return resultIDList

#read original workflow files, store into GLOBAL_ORIGINAL_WORKFLOW
def readWorkflowCSV(fileName):
    with open(fileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            traceID = each[0]
            other = each[1:len(each)]
            #[traceID,order,structtype,method1,method2,m1_para,m2_para,className1,className2, m1_return, m2_return] = each
            if traceID == 'traceID':
                continue

            traceID = int(traceID)
            if traceID not in GLOBAL_ORIGINAL_WORKFLOW:
                GLOBAL_ORIGINAL_WORKFLOW[traceID] = list()
            GLOBAL_ORIGINAL_WORKFLOW[traceID].append(other)
    return len(GLOBAL_ORIGINAL_WORKFLOW)

# filter out the selected traces , and store into reslist
def genFinalTraceList(filterTraceIDs):
    resList = list()
    newTraceID = 0
    for oldTraceId in filterTraceIDs:
        for eachTrace in GLOBAL_ORIGINAL_WORKFLOW[oldTraceId]:
            oneTrace = [newTraceID]
            oneTrace.extend(eachTrace)
            resList.append(oneTrace)
        newTraceID += 1
    return resList


def writeCSV(fileName, alist):
    with open(fileName, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)

if __name__ == "__main__":
    workflowFile = sys.argv[1]

    #tsCountList = [14, 28, 42, 56] #solo
    #tsCountList = [17, 34, 51, 68] #roller
    #tsCountList = [22, 44, 66, 88] #agilefant
    #tsCountList = [553, 1106, 1659, 2212] #xwiki
    #tsCountList = [7, 13, 20, 26] # springblog   33
    #tsCountList =[14, 28, 42, 56] #jforum    69

    allTraceCount = readWorkflowCSV(workflowFile)
    print("all:", allTraceCount)

    traceName = ['_20percent', '_40percent', '_60percent', '_80percent']
    for index in range(0, len(tsCountList)):
         selectCount = tsCountList[index]
         selectedTraceIDList = randomChoose(allTraceCount, selectCount)
         finalTraceList =genFinalTraceList(selectedTraceIDList)
         outfileName = workflowFile.split('.csv')[0] + traceName[index] + '.csv'
         writeCSV(outfileName, finalTraceList)
