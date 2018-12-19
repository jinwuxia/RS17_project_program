
'''
#from commit log, extract the commit deps(history/evolutionary coupling) for class pairs
'''
import sys
import csv
import re
import networkx as nx

#COMMIT_LOG_PRE_NAME = 'src/main/java/'  #jpetstore, bvn13_springblog
COMMIT_LOG_PRE_NAME = 'app/src/main/java/' #roller
ID2NAMEDict = dict()
NAME2IDDict = dict()
RESLIST = list()



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
                #if len(newList) >= 2:
                #    listList.append(newList)
                if len(newList) >= 1:
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
                    print commitFileName, simpleName, ','
                    if simpleName != '':
                        if simpleName not in name2IDDict:
                            name2IDDict[simpleName] = index
                            ID2NameDict[index] = simpleName
                            index += 1
                        ID = name2IDDict[simpleName]
                        newList.append(ID)
        #if len(newList) >= 2:
        #    listList.append(newList)
        if len(newList) >= 1:
            listList.append(newList)
    print 'listList=', listList
    return listList, name2IDDict, ID2NameDict



#tranverse listList, find all class's commitTimes
#return comDict[classID] = commitTimes
def classComTimes(listList):
    comDict = dict()
    for oneList in listList:
        for classID in oneList:
            if classID not in comDict:
                comDict[classID] = 1
            else:
                comDict[classID] += 1
    print 'comDict=', comDict
    return comDict

#traverse listList, find all pair-class commit times
#return PairDict[classID1][classID2]= commitTimes
def pairComTimes(listList):
    pairDict = dict()
    for oneList in listList:
        if len(oneList) == 1:
            continue
        from itertools import combinations
        tmp = list(combinations(oneList, 2))
        for each in tmp:
            [classID1, classID2] = each
            if classID1 not in pairDict:
                pairDict[classID1] = dict()
            if classID2 not in pairDict[classID1]:
                pairDict[classID1][classID2] = 1
            else:
                pairDict[classID1][classID2] += 1
    print 'pairDict=', pairDict
    return  pairDict

#according to comDict and pairDict, get direct probility of co-change
#proDict[c1][c2]= xxxxx
def directPro(comDict, pairDict):
    proDict = dict()
    for classID1 in pairDict:
        if classID1 not in proDict:
            proDict[classID1] = dict()
        for classID2 in pairDict[classID1]:
            if classID2 not in proDict:
                proDict[classID2] = dict()
            co_times = pairDict[classID1][classID2]
            proDict[classID1][classID2] = co_times / float(comDict[classID1])
            proDict[classID2][classID1] = co_times / float(comDict[classID2])
    print 'proDict=', proDict
    return proDict


#from proDict, genrate nodeList and edgeList
def createStruct(proDict):
    nodeList = list()
    edgeList = list()
    for classID1 in proDict:
        if classID1 not in nodeList:
            oneList = [classID1, ID2NAMEDict[classID1] ]
            nodeList.append(oneList)
        for classID2 in proDict[classID1]:
            if classID2 not in nodeList:
                nodeList.append([classID2, ID2NAMEDict[classID2]])

    for classID1 in proDict:
        for classID2 in proDict[classID1]:
            weight = proDict[classID1][classID2]
            edgeList.append([classID1, classID2, weight])
    print nodeList
    print edgeList
    return nodeList, edgeList

#graph
def genGraph(nodeList, edgeList):
    print "create graph"
    DG = nx.DiGraph()
    for each in nodeList:
        [classID, className] = each
        DG.add_node(classID, label=className)
    for each in edgeList:
        [classID1, classID2, weight] = each
        DG.add_edge(classID1, classID2, weight=weight)
    print 'nodes', DG.nodes()
    print 'edges', DG.edges()

    #all nodePair
    gNodeList = DG.nodes()
    pairList = list()
    for nodeID1 in gNodeList:
        for nodeID2 in gNodeList:
            if nodeID1 != nodeID2:
                pairList.append([nodeID1, nodeID2])

    #tranverse pairlist, find the weight max's path for each pair
    pairListProb = list()  #[className1, className2, prob]
    for each in pairList:
        [nodeID1, nodeID2] = each
        print 'nodeID1=', nodeID1,'nodeID2=',nodeID2
        if nx.has_path(DG, source=nodeID1, target=nodeID2):
            print 'has path'
            path = nx.shortest_path(DG, source=nodeID1, target=nodeID2)
            prob = 1.0
            for i in range(0, len(path)):
                j = i + 1
                if j < len(path):
                    #nx.get_edge_attributes(DG, 'weight')[(id1, id2)]
                    prob = prob * float(nx.get_edge_attributes(DG, 'weight')[(path[i],path[j])])


            print 'path=', path,  '   prob=',prob
            if prob > 0.3:
                RESLIST.append([nx.get_node_attributes(DG, 'label')[nodeID1], nx.get_node_attributes(DG, 'label')[nodeID2], prob])

            '''
            allPath = list(nx.all_simple_paths(DG, source=nodeID1, target=nodeID2))
            print 'allPath=',allPath
            probList = list()
            for index in range(0, len(allPath)):
                #for each path = allPath[index], compute length of path
                path = allPath[index]
                prob = 1.0
                for i in range(0, len(path)):
                    j = i + 1
                    if j < len(path):
                        #nx.get_edge_attributes(DG, 'weight')[(id1, id2)]
                        prob = prob * float(nx.get_edge_attributes(DG, 'weight')[(path[i],path[j])])
                probList.append(prob)
            maxIndex = probList.index(max(probList))
            #nx.get_node_attributes(DG, 'label')
            #print nodeID1, nodeID2, maxIndex
            print nx.get_node_attributes(DG, 'label')[nodeID1], nx.get_node_attributes(DG, 'label')[nodeID2], allPath[maxIndex], max(probList)
            RESLIST.append([nx.get_node_attributes(DG, 'label')[nodeID1], nx.get_node_attributes(DG, 'label')[nodeID2], max(probList)])
            '''
    return RESLIST


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

def writeCSV(fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(RESLIST)
    print fileName


#from commit log, extract the commit deps for class pairs
#python  input_commit_log_file_name   out_put_commit_dep_file_name    type=java,python,
if __name__ == '__main__':
    logFileName = sys.argv[1]        #input
    fileType = sys.argv[2]           #type = java,python
    outFileName = sys.argv[3]
    [commitDepList, NAME2IDDict, ID2NAMEDict] = processLog(logFileName, fileType)
    comDict = classComTimes(commitDepList)
    pairDict = pairComTimes(commitDepList)
    proDict = directPro(comDict, pairDict)
    (nodeList, edgeList) = createStruct(proDict)
    genGraph(nodeList, edgeList)
    writeCSV(outFileName)
