'''
#from commit log, extract the commit deps(history/evolutionary coupling) for class/file pairs
cochange[a,b] = cochange[b,a]  both are recorded.
'''
import sys
import csv
import re

COMMIT_LOG_PRE_NAME = list()
#COMMIT_LOG_PRE_NAME = 'src/main/java/'  #jpetstore, bvn13_springblog
#COMMIT_LOG_PRE_NAME = 'app/src/main/java/' #roller
#COMMIT_LOG_PRE_NAME = 'src/main/java/' #solor270
#COMMIT_LOG_PRE_NAME = '' #xwiki  if =null, it outputs the filename but not class name.
COMMIT_LOG_PRE_NAME.append('webapp/src/main/java/') #agilefant
COMMIT_LOG_PRE_NAME.append('src/') #agilefant

ID2NAMEDict = dict()
NAME2IDDict = dict()

GLOBLE_THR = 36
# for roller and xwiki;  0 for others.  comit-together class number > this value, ignore the dependency
'''
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
        #print fileName
    return fileName
'''
#fileName = 'dir1/dir2/filename'
def getSimpleName(fileName):
    if COMMIT_LOG_PRE_NAME[0] == '':
        return fileName

    if fileName.startswith(COMMIT_LOG_PRE_NAME[0]) == False and fileName.startswith(COMMIT_LOG_PRE_NAME[1]) == False:
        fileName = ''
    else:
        tmp = fileName.split('.java')[0]
        if fileName.startswith(COMMIT_LOG_PRE_NAME[0]):
            pre = COMMIT_LOG_PRE_NAME[0]
        else:
            pre = COMMIT_LOG_PRE_NAME[1]
        preLen = len(pre)
        tmp = tmp[preLen: len(tmp)]
        tmp = tmp.split('/')
        fileName = '.'.join(tmp)
        print (fileName)
    return fileName

'''
filter test file
'''
def isNonTest(filename):
    if "/test/" in filename:
        return False
    return True



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

    with open(fileName, encoding="utf8") as fp:
        newList = list()
        for line in fp:
            if re.match(r'commit[\s][0-9,a-z,A-Z]+', line):
                #print 'commit', line
                if len(newList) >= 2 and (GLOBLE_THR == 0 or (GLOBLE_THR > 0 and len(newList) < GLOBLE_THR )):
                    listList.append(newList)

                newList = list()
            elif re.match(r'[MAD][\t]', line):
                #print 'MAD', line
                #print line.split('\t')
                commitType = line.split('\t')[0]
                commitFileName = line.split('\t')[1] #'fileName\n'
                commitFileName = commitFileName[0:len(commitFileName) - 1]
                #print commitType, commitFileName
                if commitType == 'M' and isIncluded(commitFileName, fileType) and isNonTest(commitFileName): #just modify, not include Delete and Add
                    simpleName = getSimpleName(commitFileName)
                    if simpleName != '':
                        if simpleName not in name2IDDict:
                            name2IDDict[simpleName] = index
                            ID2NameDict[index] = simpleName
                            index += 1
                        ID = name2IDDict[simpleName]
                        newList.append(ID)
        if len(newList) >= 2 and (GLOBLE_THR == 0 or (GLOBLE_THR > 0 and len(newList) < GLOBLE_THR )):
            listList.append(newList)

    return listList, name2IDDict, ID2NameDict

#dict[classID1][classID2] = commit_times_together
#dict[classId1][classID2] is also recored,beacuse we use permutations(2), not combinations
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
    with open(fileName, 'w', newline="") as fp:  #"wb" in python2, "w" in python3
        writer = csv.writer(fp)
        writer.writerows(listList)
    print (fileName)


#from commit log, extract the commit deps for class pairs
#python  input_commit_log_file_name   out_put_commit_dep_file_name    type=java,python,
if __name__ == '__main__':
    logFileName = sys.argv[1]        #input
    commitDepFileName = sys.argv[2]  #output
    fileType = sys.argv[3]           #type = java,python
    [commitDepList, NAME2IDDict, ID2NAMEDict] = processLog(logFileName, fileType)
    commitDepDict = change2Pair(commitDepList)
    writeCSV(commitDepDict, commitDepFileName)

    #for each in commitDepList:
    #    print each
