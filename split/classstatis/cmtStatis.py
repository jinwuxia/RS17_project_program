'''
#from commit log, extract the commit deps(history/evolutionary coupling) for class file
analyze the statis data
'''
import sys
import csv
import re

COMMIT_LOG_PRE_NAME = list()
#COMMIT_LOG_PRE_NAME = 'src/main/java/'  #jpetstore, bvn13_springblog
#COMMIT_LOG_PRE_NAME = 'app/src/main/java/' #roller
#COMMIT_LOG_PRE_NAME = 'src/main/java/' #solor270
#COMMIT_LOG_PRE_NAME = '' #xwiki
COMMIT_LOG_PRE_NAME.append('webapp/src/main/java/') #agilefant
COMMIT_LOG_PRE_NAME.append('src/') #agilefant

ID2NAMEDict = dict()
NAME2IDDict = dict()

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
            #print ("line:  " + line)
            if re.match(r'commit[\s][0-9,a-z,A-Z]+', line):
                #print 'commit', line
                if len(newList) >= 1:
                    listList.append(newList)
                newList = list()
            elif re.match(r'[MAD][\t]', line):
                #print 'MAD', line
                #print line.split('\t')
                commitType = line.split('\t')[0]
                commitFileName = line.split('\t')[1] #'fileName\n'
                commitFileName = commitFileName[0:len(commitFileName) - 1]
                #print( commitType, commitFileName)
                if commitType == 'M' and isIncluded(commitFileName, fileType) and isNonTest(commitFileName): #just modify, not include Delete and Add
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

#write filenames in commit history to a file
def writeFileName(outfileName):
    import csv
    with open(outfileName, "w", newline="") as fp:
        writer = csv.writer(fp)
        for key in NAME2IDDict:
            writer.writerow([key])




#from commit log, extract the commit deps for class pairs
#python  input_commit_log_file_name     type=java,python,
if __name__ == '__main__':
    logFileName = sys.argv[1]        #input
    fileType = sys.argv[2]           #type = java,python
    [commitDepList, NAME2IDDict, ID2NAMEDict] = processLog(logFileName, fileType)

    #the filenames in commit log are more than the statis understand filename
    #only works for xwiki, since the filename complexly corressponds to class
    writeFileName("agilefantcmt_class.csv")


    #for each in commitDepList:
    #    print (each)



    lenList = list()

    for each in commitDepList:
        lenList.append(len(each))
    #print(lenList)
    print ('len of the Classcommit times:',  len(commitDepList))
    print ('involved class count:  ',  len(NAME2IDDict))
    print ('min of EachCommit Len: ',  min(lenList))
    print ('max of EachCommit Len: ',  max(lenList))
    print ('avg of EachCommit Len: ',  sum(lenList) / float(len(lenList)))



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
    print ('len of class commit times', len(newCommitDepList))
    print ('min of EachCommit Len:', min(newLenList))
    print ('max of EachCommit Len:', max(newLenList))
    print ('avg of EachCommit Len:', sum(newLenList) / float(len(newLenList)))
    print ('involved class count:  ', len(newClassList))
