import sys
import csv
import re

global g_clusterID2Interf2APIDict #[clusterID][interface] = list[api id ...]
global g_apiDict #[api id] = api object
global g_ignore_items
#api is operation
class APIObject:
    def __init__(self, clusterID, interface, apiName, itemSet):
        self.clusterID = clusterID
        self.interface = interface
        self.apiName = apiName
        self.itemSet = itemSet

def GetInterf(api):
    #interface name
    apiList = api.split('.')
    del apiList[len(apiList) - 1]
    interface = '.'.join(apiList)
    return interface

def IsIgnored(item):
    global g_ignore_items
    if item in g_ignore_items:
        return True
    else:
        return False

#for each ele, split by hump
def SplitHump(oneList):
    resList = list()
    for name in oneList:
        upperIndexList = list()
        upperIndexList.append(0) #first index
        for index in range(0, len(name)):
            if name[index].isupper():
                upperIndexList.append(index)
        upperIndexList.append(index + 1) #last index + 1

        for i in range(0, len(upperIndexList) - 1):
            index_s = upperIndexList[i]
            index_e = upperIndexList[i + 1]
            strstr = name[index_s: index_e]
            resList.append(strstr)
    return resList

#split(., tuofeng) each name to items, and ignore the non-domain item
def GetItems(nameSet):
    itemList = list()
    for name in nameSet:
        #split
        tmpList = re.split( r'[._]', name)
        tmpList = SplitHump(tmpList)
        tmpList = [each.lower() for each in tmpList]
        itemList.extend(tmpList)
    newItemList = list()
    for item in itemList:
        if IsIgnored(item) == False and item != '':
            newItemList.append(item)
    #print 'before=', nameSet
    #print 'after =', set(newItemList)
    return set(newItemList)

def ReadAPIFile(fileName):
    apiID = 0
    clusterID2Interf2ApiDict = dict()
    apiDict = dict()

    with open(fileName,'r') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [clusterID, tsID, apiName] = each
            if each[0] == 'clusterID':
                continue
            clusterID = int(clusterID)
            interface = GetInterf(apiName)
            if clusterID not in clusterID2Interf2ApiDict:
                clusterID2Interf2ApiDict[clusterID] = dict()
            if interface not in clusterID2Interf2ApiDict[clusterID]:
                clusterID2Interf2ApiDict[clusterID][interface] = list()
            nameSet = set()
            nameSet.add(apiName)
            itemSet = GetItems(nameSet)
            oneObejct = APIObject(clusterID, interface, apiName, itemSet)
            #print nameSet
            #print oneObejct.itemSet
            apiDict[apiID] = oneObejct
            clusterID2Interf2ApiDict[clusterID][interface].append(apiID)
            apiID += 1
    #print clusterID2Interf2ApiDict
    #print apiDict
    return clusterID2Interf2ApiDict, apiDict

#domain-level edge weight
def GetEdge(apiID1, apiID2):
    global g_apiDict
    #print g_apiDict
    itemSet1 = g_apiDict[apiID1].itemSet
    itemSet2 = g_apiDict[apiID2].itemSet
    #print g_apiDict[apiID1].interface, g_apiDict[apiID1].apiName, itemSet1
    #print g_apiDict[apiID2].interface, g_apiDict[apiID2].apiName, itemSet2
    '''
    if len(itemSet1) == 0 and len(itemSet2) == 0:  #not have domain items, then return 1
        edge_wei = 1
        edge_unwei = 1
    '''
    interSet = itemSet1 & itemSet2
    unionSet = itemSet1 | itemSet2
    edge_wei = len(interSet) / float(len(unionSet))
    if len(interSet) != 0:
        edge_unwei = 1.0
    else:
        edge_unwei = 0.0
    return edge_wei, edge_unwei


#compute the interface's dom_cohesion
def Metric_dom_cohesion(clusterID, interface):
    global g_clusterID2Interf2APIDict
    apiIDList = g_clusterID2Interf2APIDict[clusterID][interface]
    if len(apiIDList) == 1:
        dom_cohesion_wei = 1.0
        dom_cohesion_unwei = 1.0
    else:
        from itertools import combinations
        apiIDPairList = list(combinations(apiIDList, 2))
        fenmu = len(apiIDPairList)
        fenzi_wei = 0
        fenzi_unwei = 0
        for apiIDpair in apiIDPairList:
            [edge_wei, edge_unwei] = GetEdge(apiIDpair[0], apiIDpair[1])
            fenzi_wei += edge_wei
            fenzi_unwei += edge_unwei
        dom_cohesion_wei = fenzi_wei / float(fenmu)
        dom_cohesion_unwei = fenzi_unwei / float(fenmu)
    return dom_cohesion_wei, dom_cohesion_unwei

if __name__ == '__main__':
    apiFileName = sys.argv[1]

    global g_ignore_items
    global g_clusterID2Interf2APIDict
    global g_apiDict
    g_clusterID2Interf2APIDict = dict()
    g_apiDict = dict()
    g_ignore_items = ['java', 'net', 'org', 'util', 'lang', \
                      'math', 'string', 'int', 'void', 'date', 'object', 'list',\
                      'get', 'set', 'decimal', 'boolean']

    [g_clusterID2Interf2APIDict, g_apiDict] = ReadAPIFile(apiFileName)

    if len(g_clusterID2Interf2APIDict) == 0:
        print 'avg_dom_cohesion_wei=', 1.0, 'avg_dom_cohesion_unwei=', 1.0,
        print 'interface number=', 0
    else:
        dom_cohesion_wei_list = list()
        dom_cohesion_unwei_list = list()
        for clusterID in g_clusterID2Interf2APIDict:
            for interface in g_clusterID2Interf2APIDict[clusterID]:
                [dom_cohesion_wei, dom_cohesion_unwei] = Metric_dom_cohesion(clusterID, interface)
                dom_cohesion_wei_list.append(dom_cohesion_wei)
                dom_cohesion_unwei_list.append(dom_cohesion_unwei)
                #print clusterID, interface, dom_cohesion_wei, dom_cohesion_unwei
        avg_dom_cohesion_wei = sum(dom_cohesion_wei_list) / float(len(dom_cohesion_wei_list))
        avg_dom_cohesion_unwei = sum(dom_cohesion_unwei_list) / float(len(dom_cohesion_unwei_list))
        print 'avg_dom_cohesion_wei=', avg_dom_cohesion_wei, 'avg_dom_cohesion_unwei=', avg_dom_cohesion_unwei,

        interface_number = 0
        for clusterID in g_clusterID2Interf2APIDict:
            interface_number += len(g_clusterID2Interf2APIDict[clusterID])
        print 'interface number=', interface_number
