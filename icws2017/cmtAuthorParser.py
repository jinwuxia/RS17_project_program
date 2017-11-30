'''
#from commit log, extract the contributor coupling for class pairs
'''
import sys
import csv
import re

JPETSTORE_COMMIT_LOG_PRE_NAME = 'src/main/java/'


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

#returrn: dict[classname] = set(author1, author2, ...)
def processLog(fileName, fileType):
    class2AuthorDict = dict()  #dict[classname] = set(author1, author2, ...)
    with open(fileName) as fp:
        for line in fp:
            if re.match(r'commit[\s][0-9,a-z,A-Z]+', line):
                print 'commit', line
            elif 'Author:' in line:
                author = re.split('<|@', line)[1]
                print 'author:', author
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
                        if simpleName not in class2AuthorDict:
                            class2AuthorDict[simpleName] = set()
                        class2AuthorDict[simpleName].add(author)
    return class2AuthorDict


def getAuthorNumber(class2AuthorDict):
    authorSet= set()
    for eachClass in class2AuthorDict:
        authorSet = authorSet | class2AuthorDict[eachClass]
    print 'authorSet: ', authorSet
    print 'authorLen: ', len(authorSet)

def change2Pair(class2AuthorDict):
    listList = list()
    for class1 in class2AuthorDict.keys():
        for class2 in class2AuthorDict.keys():
            if class1 != class2:
                authorSet1 = class2AuthorDict[class1]
                authorSet2 = class2AuthorDict[class2]
                interSet = authorSet1 & authorSet2
                if len(interSet) != 0:
                    listList.append([class1, class2, len(interSet)])
    return listList

def writeCSV(listList, fileName):
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
    class2AuthorDict = processLog(logFileName, fileType)
    print 'class2AuthorDict', class2AuthorDict
    listList = change2Pair(class2AuthorDict)
    writeCSV(listList, commitDepFileName)
    getAuthorNumber(class2AuthorDict)
