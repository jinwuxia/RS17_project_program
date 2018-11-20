'''
#from commit log, extract the commit deps(history/evolutionary coupling) for class file
analyze the statis data
'''
import sys
import csv
import re

COMMIT_LOG_PRE_NAME = 'src/main/java/'  #jpetstore, bvn13_springblog
#COMMIT_LOG_PRE_NAME = 'app/src/main/java/' #roller
#COMMIT_LOG_PRE_NAME = 'src/main/java/' #solor270

#fileName = 'dir1/dir2/filename'
def getSimpleName(fileName):
    if COMMIT_LOG_PRE_NAME == '':
        return fileName
    if fileName.startswith(COMMIT_LOG_PRE_NAME) == False:
        fileName = ''
    else:
        tmp = fileName.split('.java')[0]
        preLen = len(COMMIT_LOG_PRE_NAME)
        tmp = tmp[preLen: len(tmp)]
        tmp = tmp.split('/')
        fileName = '.'.join(tmp)
        print fileName
    return fileName

def isIncluded(fileName, fileType):
    if fileType == 'python':
        return ('.py' in fileName)
    if fileType == 'java':
        return ('.java' in fileName)
    return False



#list[0] = [clasID1, clasID2, classID3.]
#Parameter_count =1, count classes in commit, even alone
#Parameter_count =2, count classes in commit, at least in pair
def processLog_M_All(fileName, fileType, parameter_count, parameter_commit_type):
    listList = list()
    name2IDDict = dict()
    ID2NameDict = dict()
    index = 0

    with open(fileName, encoding="utf8") as fp:
        newList = list()
        for line in fp:
            if re.match(r'commit[\s][0-9,a-z,A-Z]+', line):
                #print 'commit', line
                if len(newList) >= parameter_count:
                    listList.append(newList)
                if len(newList) >= parameter_count:
                    listList.append(newList)
                newList = list()
            elif re.match(r'[MAD][\t]', line):
                #print 'MAD', line
                #print line.split('\t')
                commitType = line.split('\t')[0]
                commitFileName = line.split('\t')[1] #'fileName\n'
                commitFileName = commitFileName[0:len(commitFileName) - 1]
                #print commitType, commitFileName
                if parameter_commit_type == 'M':
                    if commitType == 'M' and isIncluded(commitFileName, fileType): #just modify, not include Delete and Add
                        simpleName = getSimpleName(commitFileName)
                        if simpleName != '':
                            if simpleName not in name2IDDict:
                                name2IDDict[simpleName] = index
                                ID2NameDict[index] = simpleName
                                index += 1
                            ID = name2IDDict[simpleName]
                            newList.append(ID)

                if parameter_commit_type == 'A':
                    if commitType == 'A' and isIncluded(commitFileName, fileType): #just modify, not include Delete and Add
                        simpleName = getSimpleName(commitFileName)
                        if simpleName != '':
                            if simpleName not in name2IDDict:
                                name2IDDict[simpleName] = index
                                ID2NameDict[index] = simpleName
                                index += 1
                            ID = name2IDDict[simpleName]
                            newList.append(ID)

                if parameter_commit_type == 'AM':
                    if (commitType == 'M' or commitType == 'A') and isIncluded(commitFileName, fileType): #just modify, not include Delete and Add
                        simpleName = getSimpleName(commitFileName)
                        if simpleName != '':
                            if simpleName not in name2IDDict:
                                name2IDDict[simpleName] = index
                                ID2NameDict[index] = simpleName
                                index += 1
                            ID = name2IDDict[simpleName]
                            newList.append(ID)
        if len(newList) >= parameter_count:
            listList.append(newList)

    return listList, name2IDDict, ID2NameDict

def readClassBenchmark(fileName):
    classList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classList.append(className)
    return classList

def sumClass(listList, ID2NAMEDict, benchmarkClassList):
    classList = list()
    for aList in listList:
        for each in aList:
            if each not in classList:
                classList.append(each)
    #print classList
    count = 0
    for each in classList:
        #print ID2NAMEDict[each]
        if ID2NAMEDict[each] in benchmarkClassList:
            count += 1
    print len(classList), count
    return count

#from commit log, extract the commit deps for class pairs
#python  input_commit_log_file_name     type=java,python,
if __name__ == '__main__':
    classFileName = sys.argv[1]
    logFileName = sys.argv[2]        #input
    fileType = sys.argv[3]           #type = java,python
    #[commitDepList, NAME2IDDict, ID2NAMEDict] = processLog(logFileName, fileType)

    benchmarkClassList = readClassBenchmark(classFileName)

    [commitDepList1, NAME2IDDict1, ID2NAMEDict1] = processLog_M_All(logFileName, fileType, parameter_count=1, parameter_commit_type='A')
    classnumber1 = sumClass(commitDepList1, ID2NAMEDict1, benchmarkClassList)
    [commitDepList2, NAME2IDDict2, ID2NAMEDict2] = processLog_M_All(logFileName, fileType, parameter_count=2, parameter_commit_type='A')
    classnumber2 = sumClass(commitDepList2, ID2NAMEDict2, benchmarkClassList)
    [commitDepList3, NAME2IDDict3, ID2NAMEDict3] = processLog_M_All(logFileName, fileType, parameter_count=1, parameter_commit_type='M')
    classnumber3 = sumClass(commitDepList3, ID2NAMEDict3, benchmarkClassList)
    [commitDepList4, NAME2IDDict4, ID2NAMEDict4] = processLog_M_All(logFileName, fileType, parameter_count=2, parameter_commit_type='M')
    classnumber4 = sumClass(commitDepList4, ID2NAMEDict4, benchmarkClassList)

    [commitDepList5, NAME2IDDict5, ID2NAMEDict5] = processLog_M_All(logFileName, fileType, parameter_count=1, parameter_commit_type='AM')
    classnumber5 = sumClass(commitDepList5, ID2NAMEDict5, benchmarkClassList)
    [commitDepList6, NAME2IDDict6, ID2NAMEDict6] = processLog_M_All(logFileName, fileType, parameter_count=2, parameter_commit_type='AM')
    classnumber6 = sumClass(commitDepList6, ID2NAMEDict6, benchmarkClassList)
    #for each in commitDepList:
    #    print each

    print 'len=1, A:', classnumber1
    print 'len=2, A:', classnumber2
    print 'len=1, M:', classnumber3
    print 'len=2, M:', classnumber4
    print 'len=1, AM:', classnumber5
    print 'len=2, AM:', classnumber6

    '''
    lenList = list()
    for each in commitDepList:
        lenList.append(len(each))
    print 'len of the Classcommit times:', len(commitDepList)
    print 'involved class count:  ', len(NAME2IDDict)
    print 'min of EachCommit Len:', min(lenList)
    print 'max of EachCommit Len:', max(lenList)
    print 'avg of EachCommit Len:', sum(lenList) / float(len(lenList))
    '''

    '''
    #delete large commit beacause it is not relevant to class function evolve.
    FilterValue = 37
    newCommitDepList = list()
    newLenList = list()
    newClassList = list()
    for each in commitDepList:
        if len(each) < FilterValue:
            newCommitDepList.append(each)
            newLenList.append(len(each))
            for eachClassID in each:
                if eachClassID not in newClassList:
                    newClassList.append(eachClassID)
    print 'min of EachCommit Len:', min(newLenList)
    print 'max of EachCommit Len:', max(newLenList)
    print 'avg of EachCommit Len:', sum(newLenList) / float(len(newLenList))
    print 'involved class count:  ', len(newClassList)
    '''
