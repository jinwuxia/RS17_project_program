# -*- coding: utf-8 -*-
import sys
import csv
'''
#before make decison about how to cluster the classes,
#we compute three features first, and merge them using pre-set weight,
#observe the feature values' distribution.
#this will help us set the clustering threshold.
'''
STRUCT_MASK = '0101000110'  #Extend,Typed,Import,Call,cast,create,Implement,set,use,throw
COMMUNICATION_TYPE = 'total_freq' #call, para_num, ret_num, call_freq, para_num_freq, ret_num_freq, total, total_freq
MERGE_FUNC = 'AVG'   #class-cluster depvalue = min,max,avg

FENWEI_THR = 0.9
STRUCT_W = 0.5
COMMUN_W = 0.5
COMMIT_W = 0.0

STRUCT_DEP_DICT = dict() #dict[classname1][classname2] = depbitStr
COMMIT_DEP_DICT = dict() #dict[classname1][classname2] = commitDep
COMMUN_DEP_DICT = dict() #dict[classname1][classname2] = commuDEPClassObject
CLASSNAME2IDDict = dict()
CLASSID2NAMEDict = dict()
CLASSIDPAIRDICT = dict()   #dict[id][id] = [structdep, commitdep, commu_totaldep, commu_total_fdep, mixeddep]


class ComDep:
    def __init__(self, call, para_num, ret_num, call_freq, para_num_freq, ret_num_freq, total, total_freq):
        self.call = call
        self.para_num = para_num
        self.ret_num = ret_num
        self.call_freq = call_freq
        self.para_num_freq = para_num_freq
        self.ret_num_freq = ret_num_freq
        self.total = total
        self.total_freq = total_freq

#communicationFile=
#['className1', 'className2', 'call', 'p_num', 'r_num', 'call_f', 'p_num_f', 'r_num_f', 'total', 'total_f']
def readCommunicationDepFile(fileName):
    resDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, call, p_num, r_num, call_f, p_num_f, r_num_f, total, total_f] = each
            if className1 == 'className1':
                continue
            oneComDep = ComDep(int(call), int(p_num), int(r_num), int(call_f), int(p_num_f), int(r_num_f), int(total), int(total_f))
            if className1 not in resDict:
                resDict[className1] = dict()
            resDict[className1][className2] = oneComDep
    return resDict


#hypothisis: only call, set, use,Typed are the structure relation
def readStructDepFile(fileName):
    resDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, structBitStr] = each
            if className1 not in resDict:
                resDict[className1] = dict()
            resDict[className1][className2] = structBitStr
    return resDict

#commitFile=[[classname, classname, value],]
def readCommitDepFile(fileName):
    resDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className1, className2, commitValue] = each
            if className1 not in resDict:
                resDict[className1] = dict()
            resDict[className1][className2] = int(commitValue)
    return resDict

def genClassDict(classIndex, depDict):
    for className1 in depDict:
        if className1 not in CLASSNAME2IDDict:
            CLASSNAME2IDDict[className1] = classIndex
            CLASSID2NAMEDict[classIndex] = className1
            classIndex += 1
        classID1 = CLASSNAME2IDDict[className1]
        if classID1 not in CLASSIDPAIRDICT:
            CLASSIDPAIRDICT[classID1] = dict()

        for className2 in depDict[className1]:
            if className2 not in CLASSNAME2IDDict:
                CLASSNAME2IDDict[className2] = classIndex
                CLASSID2NAMEDict[classIndex] = className2
                classIndex += 1
            classID2 = CLASSNAME2IDDict[className2]
            if classID2 not in CLASSIDPAIRDICT[classID1]:
                CLASSIDPAIRDICT[classID1][classID2]= list()
    return classIndex

#generate CLASSNAME2IDDict, CLASSID2NAMEDict, CLASSIDPAIRDICT
def genAllClassDict():
    classIndex = 0
    classIndex = genClassDict(classIndex, STRUCT_DEP_DICT)
    classIndex = genClassDict(classIndex, COMMIT_DEP_DICT)
    classIndex = genClassDict(classIndex, COMMUN_DEP_DICT)


#communType decides which type is chosed
def getCommunDepBetClass(classID1, classID2, communType):
    className1 = CLASSID2NAMEDict[classID1]
    className2 = CLASSID2NAMEDict[classID2]
    communicationValue = 0
    if className1 in COMMUN_DEP_DICT:
        if className2 in COMMUN_DEP_DICT[className1]:
            oneComDep = COMMUN_DEP_DICT[className1][className2]
            if communType == 'call':
                communicationValue = oneComDep.call
            elif communType == 'para_num':
                communicationValue = oneComDep.para_num
            elif communType == 'ret_num':
                communicationValue = oneComDep.ret_num
            elif communType == 'total':
                communicationValue = oneComDep.total
            elif communType == 'call_freq':
                communicationValue = oneComDep.call_freq
            elif communType == 'para_num_freq':
                communicationValue = oneComDep.para_num_freq
            elif communType == 'ret_num_freq':
                communicationValue = oneComDep.ret_num_freq
            elif communType == 'total_freq':
                communicationValue = oneComDep.total_freq
    return communicationValue

def getCommitDepBetClass(classID1, classID2):
    commitValue = 0
    className1 = CLASSID2NAMEDict[classID1]
    className2 = CLASSID2NAMEDict[classID2]
    if className1 in COMMIT_DEP_DICT:
        if className2 in COMMIT_DEP_DICT[className1]:
            commitValue = COMMIT_DEP_DICT[className1][className2]
    return commitValue

#STRUCT_MASK   decides which struct_dep is chosed
def getStructDepBetClass(classID1, classID2):
    className1 = CLASSID2NAMEDict[classID1]
    className2 = CLASSID2NAMEDict[classID2]
    structValue = 0
    if className1 in STRUCT_DEP_DICT:
        if className2 in STRUCT_DEP_DICT[className1]:
            structBitStr = STRUCT_DEP_DICT[className1][className2]
            for index in range(0, len(structBitStr)):
                if STRUCT_MASK[index] == '1' and structBitStr[index] == '1':
                    structValue += 1
    return structValue

#compute CLASSIDPAIRDICT
def getAllDep():
    for classID1 in CLASSIDPAIRDICT:
        for classID2 in CLASSIDPAIRDICT[classID1]:
            structValue = getStructDepBetClass(classID1, classID2)
            commitValue = getCommitDepBetClass(classID1, classID2)
            communValue = getCommunDepBetClass(classID1, classID2, COMMUNICATION_TYPE)
            mixedValue = 0
            CLASSIDPAIRDICT[classID1][classID2].extend([structValue, commitValue, communValue, mixedValue])
            #print classID1, classID2, structValue, commitValue, communValue

#min-max 归一化,   use 90% value as the max, leave out the noise
def normalizedMinMax(oneList):
    resList = list()
    fenweiIndex = int(len(oneList) * FENWEI_THR)
    sortedList = sorted(oneList)
    maxValue= sortedList[fenweiIndex]
    minValue = min(oneList)
    for each in oneList:
        if each > maxValue:
            each = maxValue
        tmp = (each - minValue) / float(maxValue - minValue)
        tmp = round(tmp, 5)
        #print minValue, maxValue, each, tmp
        resList.append(tmp)
    return resList

#均值-方差归一化
def normalizedMeanStd(oneList):
    resList = list()
    import numpy as np
    mean = np.average(oneList)
    sigma = np.std(oneList)
    for each in oneList:
        tmp = (each - mean) / float(sigma)
        tmp = round(tmp, 5)
        #print mean, sigma, each, tmp
        resList.append(tmp)
    return resList

#normalized CLASSIDPAIRDICT and compute mixedValue
def normCalMixedDep():
    structList = list()
    commitList = list()
    communList = list()
    for classID1 in CLASSIDPAIRDICT:
        for classID2 in CLASSIDPAIRDICT[classID1]:
            structList.append(CLASSIDPAIRDICT[classID1][classID2][0])
            commitList.append(CLASSIDPAIRDICT[classID1][classID2][1])
            communList.append(CLASSIDPAIRDICT[classID1][classID2][2])
    #print structList,'\n'
    #print commitList,'\n'
    #print communList,'\n'
    if sum(structList) > 0.00001:
        structList = normalizedMinMax(structList)
    if sum(commitList) > 0.00001:
         commitList= normalizedMinMax(commitList)
    if sum(communList) > 0.00001:
        communList = normalizedMinMax(communList)
    #print structList,'\n'
    #print commitList,'\n'
    #print communList,'\n'

    index = 0
    for classID1 in CLASSIDPAIRDICT:
        for classID2 in CLASSIDPAIRDICT[classID1]:
            CLASSIDPAIRDICT[classID1][classID2][0] = structList[index]
            CLASSIDPAIRDICT[classID1][classID2][1] = commitList[index]
            CLASSIDPAIRDICT[classID1][classID2][2] = communList[index]
            CLASSIDPAIRDICT[classID1][classID2][3] = structList[index] * STRUCT_W + commitList[index] * COMMIT_W + communList[index] * COMMUN_W
            CLASSIDPAIRDICT[classID1][classID2][3] = round(CLASSIDPAIRDICT[classID1][classID2][3], 5)
            index += 1

#write CLASSIDPAIRDICT to file
def writeDict2CSV(fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        for classID1 in CLASSIDPAIRDICT:
            for classID2 in CLASSIDPAIRDICT[classID1]:
                tmpList = list()
                depList = CLASSIDPAIRDICT[classID1][classID2]
                tmpList.append(CLASSID2NAMEDict[classID1])
                tmpList.append(CLASSID2NAMEDict[classID2])
                tmpList.extend(depList)
                writer.writerow(tmpList)
    print fileName

def readClassListFile(fileName):
    resList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [classID, className] = each
            resList.append(className)
    return resList

def filterDep(classList):
    resList = list()
    for classID1 in CLASSIDPAIRDICT:
        className1 = CLASSID2NAMEDict[classID1]
        if className1 in classList:
            for classID2 in CLASSIDPAIRDICT[classID1]:
                className2 = CLASSID2NAMEDict[classID2]
                if className2 in classList:
                    tmpList = list()
                    depList = CLASSIDPAIRDICT[classID1][classID2]
                    tmpList.append(className1)
                    tmpList.append(className2)
                    tmpList.extend(depList)
                    resList.append(tmpList )
    return resList


def writeCSV(fileName, resList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    print fileName

#before make decison about how to cluster the classes,
#we compute three features first, and merge them using pre-set weight,
#observe the feature values' distribution.
#this will help us set the clustering threshold.
#python pro.py   struct.csv  commit.csv  commun.csv  classList.csv out.csv
if __name__ == '__main__':
    structDepFileName = sys.argv[1]
    commitDepFileName = sys.argv[2]
    communDepFileName = sys.argv[3]
    classListFileName = sys.argv[4]
    outfileName = sys.argv[5]
    if structDepFileName != 'null':
        STRUCT_DEP_DICT = readStructDepFile(structDepFileName)
        #print STRUCT_DEP_DICT, '\n'
    if commitDepFileName != 'null':
        COMMIT_DEP_DICT = readCommitDepFile(commitDepFileName)
        #print COMMIT_DEP_DICT, '\n'
    if communDepFileName != 'null':
        COMMUN_DEP_DICT = readCommunicationDepFile(communDepFileName)
        #print COMMUN_DEP_DICT, '\n'
    if classListFileName != 'null':
        classList = readClassListFile(classListFileName)

    #generate CLASSNAME2IDDict, CLASSID2NAMEDict, and empty CLASSIDPAIRDICT
    genAllClassDict()
    #set  CLASSIDPAIRDICT with structDep, commitDep, communDep, but mixedDep =0
    getAllDep()
    #set mixedDep: normalized and compute mixed value in CLASSIDPAIRDICT
    normCalMixedDep()

    if classListFileName == 'null':
        writeDict2CSV(outfileName)
    else:
        resList = filterDep(classList)
        writeCSV(outfileName, resList)
