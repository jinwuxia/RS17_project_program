'''
#from commit log, extract the commit deps(history/evolutionary coupling) for class pairs
'''
import sys
import csv
import re

JPETSTORE_COMMIT_LOG_PRE_NAME = 'src/main/java/'
ID2NAMEDict = dict()
NAME2IDDict = dict()

#fileName = 'dir1/dir2/filename'
def getSimpleName(fileName):
    if JPETSTORE_COMMIT_LOG_PRE_NAME == '':
        return fileName

    else:
        if JPETSTORE_COMMIT_LOG_PRE_NAME in fileName:
            tmp = fileName.split('.java')[0]
            preLen = len(JPETSTORE_COMMIT_LOG_PRE_NAME)
            tmp = tmp[preLen: len(tmp)]
            tmp = tmp.split('/')
            fileName = '.'.join(tmp)
            print fileName
        else:
            fileName = ''
        return fileName




def isIncluded(fileName, fileType):
    if fileType == 'python':
        return ('.py' in fileName)
    if fileType == 'java':
        return ('.java' in fileName)
    return False

#list[0] = [clasID1, clasID2, classID3.]
def processLog(fileName, fileType):
    listList = list()
    name2IDDict = dict()
    ID2NameDict = dict()
    index = 0

    with open(fileName) as fp:
        newList = list()
        for line in fp:
            if re.match(r'commit[\s][0-9,a-z,A-Z]+', line):
                #print 'commit', line
                if len(newList) >= 2:
                    listList.append(newList)
                newList = list()
            elif re.match(r'[MAD][\t]', line):
                #print 'MAD', line
                #print line.split('\t')
                commitType = line.split('\t')[0]
                commitFileName = line.split('\t')[1] #'fileName\n'
                commitFileName = commitFileName[0:len(commitFileName) - 1]
                print commitType, commitFileName
                if commitType == 'M' and isIncluded(commitFileName, fileType): #just modify, not include Delete and Add
                    simpleName = getSimpleName(commitFileName)
                    if simpleName != '':
                        if simpleName not in name2IDDict:
                            name2IDDict[simpleName] = index
                            ID2NameDict[index] = simpleName
                            index += 1
                        ID = name2IDDict[simpleName]
                        newList.append(ID)
        if len(newList) >= 2:
            listList.append(newList)

    return listList, name2IDDict, ID2NameDict

#dict[classID1][classID2] = commit_times_together
def change2Pair(listList):
    commitDict = dict()
    for eachList in listList:
        from itertools import permutations
        tmp = list(permutations(eachList, 2))
        for each in tmp:
            [id1, id2] = each
            if id1 not in commitDict:
                commitDict[id1] = dict()
            if id2 not in commitDict[id1]:
                commitDict[id1][id2] = 1
            else:
                commitDict[id1][id2] += 1

    return commitDict

def writeCSV(oneDict, fileName):
    listList = list()
    for ID1 in oneDict:
        for ID2 in oneDict[ID1]:
            listList.append([ID2NAMEDict[ID1], ID2NAMEDict[ID2], oneDict[ID1][ID2] ])
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print fileName


#from commit log, extract the commit deps for class pairs
#python  input_commit_log_file_name   out_put_commit_dep_file_name    type=java,python,
if __name__ == '__main__':
    logFileName = sys.argv[1]        #input
    commitDepFileName = sys.argv[2]  #output
    fileType = sys.argv[3]           #type = java,python
    [commitDepList, NAME2IDDict, ID2NAMEDict] = processLog(logFileName, fileType)
    commitDepDict = change2Pair(commitDepList)
    writeCSV(commitDepDict, commitDepFileName)

    for each in commitDepList:
        print each
