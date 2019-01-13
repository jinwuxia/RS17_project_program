'''
measure each service's icf_i metric and ecf_i metric,
output the final icf, ecf, and rei in avg.
'''

import sys
import csv


#note: input file includes a->b, and also b->a
def readCommit(fileName):
    commitDict = dict()
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [class1, class2, commit] = each
            if class1 not in commitDict:
                commitDict[class1] = dict()
            commitDict[class1][class2] = int(commit)
    return commitDict

#[serviceID] = [class1, class2, ...]
def readCluster(fileName, fileType):
    class2serviceDict = dict()
    serviceDict = dict()
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            if each[0] == 'classID':
                continue
            if fileType == 'fome':
                [classID, className, serviceID] = each
            else:
                [contain, serviceID, className] = each
            if serviceID not in serviceDict:
                serviceDict[serviceID] = list()
            serviceDict[serviceID].append(className)

            if className not in class2serviceDict:
                class2serviceDict[className] = list()
            class2serviceDict[className].append(serviceID)
    return serviceDict, class2serviceDict

#filter our repeat class
#dict[repeatclassname] = [serviceID1, serviceid2, ...]
def getRepeatClass(class2serviceDict):
    repeatClassDict = dict()
    for className in class2serviceDict:
        if len(class2serviceDict[className]) > 1:
            repeatClassDict[className] = class2serviceDict[className]
    return repeatClassDict


def getMin(aList):
    return min(aList)

def getMax(aList):
    return max(aList)

#junzhi
def getAvg(aList):
    return round(sum(aList) / float(len(aList)), 4)

#zhongweishu
def getMed(aList):
    if len(aList) == 0:
        return 0
    if len(aList) == 1:
        return aList[0]
    aList.sort()
    if len(aList) % 2 == 1:
        index = int(len(aList) / 2)
        return aList[index]
    else:
        index = int(len(aList) / 2)
        return ( aList[index - 1] + aList[index] ) / float(2)

def mathMetric(resList):
    minV = getMin(resList)
    maxV = getMax(resList)
    avgV = getAvg(resList)
    midV = getMed(resList)
    [pre4V, post4V] = getFour(resList)
    return avgV, minV, maxV, pre4V, midV, post4V

#1/4,  3/4
def getFour(aList):
    aList.sort()
    mid_index = int(len(aList) / 2)
    preList = aList[0: mid_index]
    postList = aList[mid_index: len(aList)]

    pre_four = getMed(preList)
    post_four = getMed(postList)
    return pre_four, post_four

#wrong
# when class1=class2, the co-change = 1, totoal = n*n groups
def intraCoWei_wrong(serviceID, serviceDict, commitDict):
    resList = list()
    for class1 in serviceDict[serviceID]:
        for class2 in serviceDict[serviceID]:
            if class1 == class2: #notice here
                res = 1
            elif (class1 in commitDict) and (class2 in commitDict[class1]):
                res = commitDict[class1][class2]
            else:
                res = 0
            resList.append(res)

    [avgV, minV, maxV, pre4V, midV, post4V] = mathMetric(resList)
    return [avgV, minV, maxV, pre4V, midV, post4V]

#correct,  size=1, then icf_{i} = 0
# when class1=class2, the co-change = 0, total n*(n-1)groups
def intraCoWei_correct(serviceID, serviceDict, commitDict):
    resList = list()
    for class1 in serviceDict[serviceID]:
        for class2 in serviceDict[serviceID]:
            if (class1 in commitDict) and (class2 in commitDict[class1]):
                res = commitDict[class1][class2]
            else: #when size =1, class1=class2, res=0
                res = 0
            resList.append(res)

    [avgV, minV, maxV, pre4V, midV, post4V] = mathMetric(resList)
    return [avgV, minV, maxV, pre4V, midV, post4V]


def isNotCount(class1,class2, flagDict):
    if class1 in flagDict and class2 in flagDict[class1]:
        return False
    return True

def addFlag(class1,class2, flagDict):
    if class1 not in flagDict:
        flagDict[class1] = dict()
    flagDict[class1][class2] = 1

    if class2 not in flagDict:
        flagDict[class2]= dict()
    flagDict[class2][class1] = 1
    return flagDict

#consifer both class is repeated, and not repeated.
#init flagDict = null
def interCoWei_original(serviceID1, serviceID2,  serviceDict, commitDict, repeatClassDict, flagDict):
    resList = list()
    for class1 in serviceDict[serviceID1]:
        for class2 in serviceDict[serviceID2]:
            res=0
            if class1 == class2:
                res = 0
            elif class1 not in repeatClassDict and class2 not in repeatClassDict:
                if class1 in commitDict and class2 in commitDict[class1]:
                    res = commitDict[class1][class2]
                else:
                    res = 0
            elif class1 in repeatClassDict or class2 in repeatClassDict:
                if isNotCount(class1, class2, flagDict):
                    if class1 in commitDict and class2 in commitDict[class1]:
                        res = commitDict[class1][class2]
                    else:
                        res = 0
                    flagDict = addFlag(class1,class2, flagDict)
                else:
                    res = 0
            resList.append(res)

    #[avgV, minV, maxV, pre4V, midV, post4V] = mathMetric(resList)
    #return [avgV, minV, maxV, pre4V, midV, post4V, flagDict]
    return resList

def computeCochangeAsnormal(class1, class2, commitDict):
    res = 0
    if class1 in commitDict and class2 in commitDict[class1]:
        res = commitDict[class1][class2]
    else:
        res = 0
    return res

'''
1)if s1:c1 not repeat, s2:c2 not repeat,
2)if s1:c1 repeat      s2:c2 not repeat,
both compute as normal

3)if s1:c1 not repeat s2:c2 repeat,
4)if s1:c1 repeat,    s2:c2 repeat.
both as follwing:
case 1: c1->c2 all apears in s1. then, co-commit = 0(include the case; c1=c2)
case 2: c1->c2 appears in flag(be counted), then co-commit =0
case 3: others: normal prcess. add flag
'''
def interCoWei_correct(serviceID1, serviceID2,  serviceDict, commitDict, repeatClassDict, flagDict):
    resList = list()
    for class1 in serviceDict[serviceID1]:
        for class2 in serviceDict[serviceID2]:
            res=0
            if class2 not in repeatClassDict: #compute as normal
                res = computeCochangeAsnormal(class1, class2, commitDict)
            elif class1 in serviceDict[serviceID1] and class2 in serviceDict[serviceID1]:
                res = 0
            elif class1 in flagDict and class2 in flagDict[class1]:
                res = 0
            else:
                res = computeCochangeAsnormal(class1, class2, commitDict)
                flagDict = addFlag_correct(class1, class2, flagDict)
            resList.append(res)

    #[avgV, minV, maxV, pre4V, midV, post4V] = mathMetric(resList)
    #return [avgV, minV, maxV, pre4V, midV, post4V, flagDict]
    return resList



def addFlag_correct(class1,class2, flagDict):
    if class1 not in flagDict:
        flagDict[class1] = dict()
    flagDict[class1][class2] = 1
    return flagDict

def statis_old(serviceDict, commitDict, repeatClassDict):
    totalTitle= list() #id1,id2,id3,..., avg
    totalSize = list()
    totalIcf_avg = list()
    totalecf_avg = list()

    for serviceID1 in serviceDict:
        size = len(serviceDict[serviceID1])
        totalTitle.append(serviceID1)
        totalSize.append(size)
        #icf
        [avgV,minV, maxV, pre4V, midV, post4V] = intraCoWei_wrong(serviceID1, serviceDict, commitDict)
        totalIcf_avg.append(avgV)
        #ecf
        valuelist=list()
        flagDict = dict() # (class1, class2) in dict,  class2 is repeat class
        for serviceID2 in serviceDict:
            if serviceID1 != serviceID2:
                tmplist= interCoWei_original(serviceID1, serviceID2, serviceDict, commitDict, repeatClassDict, flagDict)
                valuelist.extend(tmplist)
        avg_ecf = sum(valuelist) / float(len(valuelist))
        totalecf_avg.append(avg_ecf)

    summarizeList = [totalTitle, totalSize, totalIcf_avg, totalecf_avg]
    return summarizeList


def statis_new(serviceDict, commitDict, repeatClassDict):
    totalTitle= list() #id1,id2,id3,..., avg
    totalSize = list()
    totalIcf_avg = list()
    totalecf_avg = list()

    for serviceID1 in serviceDict:
        size = len(serviceDict[serviceID1])
        totalTitle.append(serviceID1)
        totalSize.append(size)

        #icf of this service
        #if size = 1, icf = 0. this is self-contained in intraCoWei_correct
        [avgV,minV, maxV, pre4V, midV, post4V] = intraCoWei_correct(serviceID1, serviceDict, commitDict)
        totalIcf_avg.append(avgV)

        #ecf of this service
        #if size == 1, then ecf = 1, it is sured to co-change with others.
        if size == 1:
            avg_ecf = 1.0
        else:
            valuelist=list()
            flagDict = dict() # (class1, class2) in dict,  class2 is repeat class
            for serviceID2 in serviceDict:
                if serviceID1 != serviceID2:
                    tmplist= interCoWei_correct(serviceID1, serviceID2, serviceDict, commitDict, repeatClassDict, flagDict)
                    valuelist.extend(tmplist)
            avg_ecf = sum(valuelist) / float(len(valuelist))
        totalecf_avg.append(avg_ecf)

    summarizeList = [totalTitle, totalSize, totalIcf_avg, totalecf_avg]
    return summarizeList


def readFileList(filename):
    alist = list()
    with open(filename, 'r', newline='') as fp:
        reader = csv.reader(fp)
        for each in reader:
            #[servicefile, apifile] = each
            servicefile = each[0]
            alist.append(servicefile)
    return alist

#python cochange_1.py
#../testcase_data/jpetstore6/dependency/jpetstore6cmt.csv
#../../FoME/services/jpetstore/FoME/jpetstore_service_4.csv
#fome
#filelist
if __name__ == '__main__':
    commitFileName  = sys.argv[1]
    fileType = sys.argv[2] #fome,other
    beprocessedFile = sys.argv[3] #serviceFile  list
    file_detail = sys.argv[4]
    file_final = sys.argv[5]
    #commitDict[class1][class2]= commitTimes
    commitDict = readCommit(commitFileName)
    clusterfileList = readFileList(beprocessedFile)

    ''' delete the old one
    fp_old = open(file_old, "w", newline="")
    writer_old = csv.writer(fp_old)
    for each in beprocessedList:
        serviceFileName = each[0]
        #serviceDict[serviceID] = [class1, class2, ...]
        [serviceDict, class2serviceDict] = readCluster(serviceFileName, fileType)
        repeatClassDict = getRepeatClass(class2serviceDict)
        summarizeList = statis_old(serviceDict, commitDict, repeatClassDict)
        writer_old.writerow([serviceFileName])
        writer_old.writerows(summarizeList)
    fp_old.close()
    '''


    fp_detail = open(file_detail, "w", newline="")
    writer_detail = csv.writer(fp_detail)
    fp_final = open(file_final, "w", newline='')
    writer_final = csv.writer(fp_final)
    for each in clusterfileList:
        serviceFileName = each
        #serviceDict[serviceID] = [class1, class2, ...]
        [serviceDict, class2serviceDict] = readCluster(serviceFileName, fileType)
        repeatClassDict = getRepeatClass(class2serviceDict)

        #store icf, ecf value for each service
        summarizeList = statis_new(serviceDict, commitDict, repeatClassDict)
        #writer_detail.writerow([serviceFileName])
        writer_detail.writerows(summarizeList)

        #store the final avg value for the system
        icfList = summarizeList[2]
        ecfList = summarizeList[3]
        final_ICF = sum(icfList) / float(len(icfList))
        final_ECF = sum(ecfList) / float(len(ecfList))
        #if final_ICF < 0.00001:
        #    final_REI = 9999999
        #else:
        final_REI = final_ECF / float(final_ICF)
        writer_final.writerow([final_ICF, final_ECF, final_REI])


        #print detail
        print(serviceFileName)
        [list1, list2, icf_list1, ecf_list1] = summarizeList
        print('icf detail:')
        for each in icf_list1:
            print(each)
        print('\n\necf detail:')
        for each in ecf_list1:
            print(each)


    fp_detail.close()
    fp_final.close()
