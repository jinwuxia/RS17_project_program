
import sys
import csv
from treelib import Node, Tree

METHODList = list() #[methodID] = Method()
TRACEList = list()  #[traceID] = list()=[ edge1, edge2 ...]

class Method:
    def __init__(self, ID, longname, shortname, tag):
        self.ID = ID
        self.longname = longname #has paralist
        self.shortname = shortname #has paralist
        #10 figures, if no high bit, then fill 0, beacause tree will sort it automatically in alphabetic order
        self.currtag = tag #tmp value, is is string XXXXXXXXXX
class Edge:
    def __init__(self, startID, endID):
        self.startID = startID
        self.endID = endID

# methodname_full.(prafulltype, parafulltype)
def GetLongName(methodName, para):
    if para == '':
        post = '()'
    else:
        post = '(' + para + ')'

    return methodName + post

#paraList = ['A.B.C', 'D.E.F'], return ['B.C','E.F']
def GetShortList(paraList):
    oneList = list()
    for para in paraList:
        arr = para.split('.')
        if len(arr) > 2:
            shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
        else:
            shortname = para
        oneList.append(shortname)

    return oneList


# methodname_short(prashorrtype, parashottype)
def GetShortName(methodName, para):
    arr = methodName.split('.')
    if len(arr) >= 2:
        shortname = arr[len(arr) - 2] + '.' + arr[len(arr) - 1]
    else:
        shortname = methodName

    if para == '':
        post = '()'
    else:
        paraList = para.split(',')
        shortParaList = GetShortList(paraList)
        post = '('  + ','.join(shortParaList) + ')'

    return shortname + post


def ReadCSV(filename):
    methodIndex = 0
    tmpMethodDict = dict() #dict(methodname) = ID

    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            #print each
            [traceID, order, structtype, startMethodName, endMethodName, m1_para, m2_para, class1, class2] = each
            startLongName = GetLongName(startMethodName, m1_para)
            endLongName = GetLongName(endMethodName, m2_para)
            startShortName = GetShortName(startMethodName, m1_para)
            endShortName = GetShortName(endMethodName, m2_para)

            if traceID == 'traceID':
                continue

            if startLongName not in tmpMethodDict:
                tmpMethodDict[startLongName] = methodIndex
                oneMethod = Method(methodIndex, startLongName, startShortName, "NULL")
                METHODList.append(oneMethod)
                methodIndex += 1
            if endLongName not in tmpMethodDict:
                tmpMethodDict[endLongName] = methodIndex
                oneMethod = Method(methodIndex, endLongName, endShortName, "NULL")
                METHODList.append(oneMethod)
                methodIndex += 1

            startID = tmpMethodDict[startLongName]
            endID = tmpMethodDict[endLongName]
            oneEdge = Edge(startID, endID)
            currentLen = len(TRACEList)
            if int(traceID) == currentLen:
                TRACEList.append(list())
            TRACEList[int(traceID)].append(oneEdge)


def ClearMethodTag():
    for index in range(0, len(METHODList)):
        METHODList[index].currtag = 'NULL'

#transform integer into string and high bit is set 0
def ToStr(num):
    onestr = str(num)
    highstr = ''
    if len(onestr) < 10:
        plusArr = ['0'] * (10 - len(onestr))
        highstr = ''.join(plusArr)
    return highstr + onestr

# for each trace otr workflow, generate callTree in order to store and visulize the workflow
# the edge order in edgeList represents the calling order, so donnot change the order.
# use tagInt to retain the order
# one trace pr workflow is a single-root tree.
# if the created fails, maybe beacause the trace has more than one root
# in one workflow, method with samename always appear more than 1 times, it's normal. so its tag always change,
# but its parent always is the newest tag of callermethod
def GenWorkflowTree(edgeList):
    tagInt = 0
    root = True

    for eachEdge in edgeList:
        startID = eachEdge.startID
        endID = eachEdge.endID

        #process the root of the tree
        if root == True:
            onetree = Tree()
            METHODList[startID].currtag = ToStr(tagInt)
            onetree.create_node(ToStr(tagInt), ToStr(tagInt), data = METHODList[startID])
            tagInt += 1
            root = False

        #only process the callee
        if METHODList[startID].currtag == 'NULL':
            print "[ERROR]: Another root comes up -  ", METHODList[startID].longname, "\n\n"
        METHODList[endID].currtag = ToStr(tagInt)
        tagInt += 1
        #print METHODList[startID].currtag, "X", METHODList[startID].shortname, '----->', METHODList[endID].currtag, "X", METHODList[endID].shortname, "\n"

        onetree.create_node(METHODList[endID].currtag, METHODList[endID].currtag, parent = METHODList[startID].currtag, data = METHODList[endID])

    #onetree.show(data_property = 'shortname')
    return onetree



def GenMultiTree():
    treeList = list()
    for traceID in range(0, len(TRACEList)):
        edgeList = TRACEList[traceID]
        ClearMethodTag()
        onetree = GenWorkflowTree(edgeList)
        treeList.append(onetree)
        print '# ' + str(traceID) + ':' + onetree.get_node('0000000000').data.shortname

    return treeList


def writeTree(outfileName, treeList, treeType):
    print outfileName

    for traceID in range(0, len(treeList)):
        fp = open(outfileName, 'a')
        fp.write('# ' + str(traceID) + '\n')
        fp.close()
        treeList[traceID].save2file(outfileName, data_property = treeType)




#python pro.py  workflow.csv  shortname or longname
if __name__ == '__main__':
    workflowFilename = sys.argv[1] # ../RS17_source_data/RS17_jpetstore/dynamic/source/jpetstore6_trace_method_workflow.csv
    treeType = sys.argv[2] #shortname or longname

    arr = workflowFilename.split('/')
    tmp = arr.pop()
    project = tmp.split('_')[0]
    outFileNamePre = '/'.join(arr) + '/' + project + '_'

    ReadCSV(workflowFilename)
    treeList = GenMultiTree()

    outfileName = outFileNamePre + 'workflow_' + treeType + '.tree'
    writeTree(outfileName, treeList, treeType)
