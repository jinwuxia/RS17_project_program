import sys
import csv

global g_clusterID2Interf2APIDict #[clusterID][interface] = list[api id ...]
global g_apiDict #[api id] = api object

#api is operation
class APIObject:
    def __init__(self, clusterID, interface, apiName, parameterSet, returnSet):
        self.clusterID = clusterID
        self.interface = interface
        self.apiName = apiName
        self.parameterSet = parameterSet
        self.returnSet = returnSet

def Trans2Set(strstr):
    if strstr == '':
        resList = ['void']
    else:
        resList = strstr.split(',')
    return set(resList)

def GetInterf(api):
    #interface name
    apiList = api.split('.')
    del apiList[len(apiList) - 1]
    interface = '.'.join(apiList)
    return interface

def ReadAPIFile(fileName):
    apiID = 0
    clusterID2Interf2ApiDict = dict()
    apiDict = dict()

    with open(fileName,'r') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [clusterID, apiName, parameterstr, returnstr] = each
            if each[0] == 'clusterID':
                continue
            clusterID = int(clusterID)
            parameterSet = Trans2Set(parameterstr)
            returnSet = Trans2Set(returnstr)
            interface = GetInterf(apiName)
            if clusterID not in clusterID2Interf2ApiDict:
                clusterID2Interf2ApiDict[clusterID] = dict()
            if interface not in clusterID2Interf2ApiDict[clusterID]:
                clusterID2Interf2ApiDict[clusterID][interface] = list()
            oneObejct = APIObject(clusterID, interface, apiName, parameterSet, returnSet)
            apiDict[apiID] = oneObejct
            clusterID2Interf2ApiDict[clusterID][interface].append(apiID)
            apiID += 1
    #print clusterID2Interf2ApiDict
    #print apiDict
    return clusterID2Interf2ApiDict, apiDict


def GetIntersect(apiID1, apiID2):
    global g_apiDict
    para_interset = g_apiDict[apiID1].parameterSet & g_apiDict[apiID2].parameterSet
    return_interset = g_apiDict[apiID1].returnSet & g_apiDict[apiID2].returnSet
    return para_interset, return_interset


def GetUnionset(apiID1, apiID2):
    global g_apiDict
    para_unionset = g_apiDict[apiID1].parameterSet | g_apiDict[apiID2].parameterSet
    return_unionset = g_apiDict[apiID1].returnSet | g_apiDict[apiID2].returnSet
    return para_unionset, return_unionset


#compute the edge between two apis
#if have common para/return type, then have an edge between the two operations/apis
def GetEdge_half(interSet, unionSet):
    edge_unwei = 0
    edge_wei = 0
    if len(interSet) != 0:
        edge_unwei = 1
        edge_wei = len(interSet) / float(len(unionSet))
    #print edge_unwei, edge_wei
    return edge_unwei, edge_wei



#measure the meg-level 's interface cohesion'
def Metric_msg_cohesion(clusterID, interface):
    global g_clusterID2Interf2APIDict
    apiIDList = g_clusterID2Interf2APIDict[clusterID][interface]
    if len(apiIDList) == 1:
        cohesion_wei = 1
        cohesion_unwei= 1
    else:
        from itertools import combinations
        apiIDPairList = list(combinations(apiIDList, 2))
        fenmu = len(apiIDPairList)  #perfect graph's edge number

        fenzi_para_unweight = 0
        fenzi_para_weight = 0
        fenzi_return_unweight = 0
        fenzi_return_weight = 0
        for apiPair in apiIDPairList:
            [para_interset, return_interset] = GetIntersect(apiPair[0], apiPair[1])
            [para_unionset, return_unionset] = GetUnionset(apiPair[0], apiPair[1])

            [para_unweight, para_weight] = GetEdge_half(para_interset, para_unionset)
            fenzi_para_weight += para_weight
            fenzi_para_unweight += para_unweight

            [return_unweight, return_weight] = GetEdge_half(return_interset, return_unionset)
            fenzi_return_weight += return_weight
            fenzi_return_unweight += return_unweight

        fenzi_unweight = (fenzi_para_unweight + fenzi_return_unweight) / float(2.0)
        fenzi_weight  = (fenzi_para_weight + fenzi_return_weight) / float(2.0)
        cohesion_unwei = fenzi_unweight / float(fenmu)
        cohesion_wei = fenzi_weight / float(fenmu)

    return cohesion_wei, cohesion_unwei




if __name__ == '__main__':
    apiFileName = sys.argv[1]

    global g_clusterID2Interf2APIDict #[clusterID][interface] = [api id ....]
    global g_apiDict

    [g_clusterID2Interf2APIDict, g_apiDict] = ReadAPIFile(apiFileName)
    msg_cohesion_wei_list = list()
    msg_cohesion_unwei_list = list()

    if len(g_clusterID2Interf2APIDict) == 0:
        print  'msg_avg_wei=', 1, 'msg_avg_unwei', 1
    else:
        for clusterID in g_clusterID2Interf2APIDict:
            for interface in g_clusterID2Interf2APIDict[clusterID]:
                [msg_cohesion_wei, msg_cohesion_unwei] = Metric_msg_cohesion(clusterID, interface)
                #print str(clusterID) + ',' + interface + ',' + str(msg_cohesion_wei) + ',' +  str(msg_cohesion_unwei)
                msg_cohesion_wei_list.append(msg_cohesion_wei)
                msg_cohesion_unwei_list.append(msg_cohesion_unwei)
        msg_avg_wei = sum(msg_cohesion_wei_list) / float(len(msg_cohesion_wei_list))
        msg_avg_unwei = sum(msg_cohesion_unwei_list) / float(len(msg_cohesion_unwei_list))
        print 'msg_avg_wei=', msg_avg_wei, 'msg_avg_unwei', msg_avg_unwei

        interface_number = 0
        for clusterID in g_clusterID2Interf2APIDict:
            interface_number += len(g_clusterID2Interf2APIDict[clusterID])
        print 'interface number=', interface_number
