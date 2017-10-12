import sys
import csv
g_clusterID2InterfDict = dict() #[clusterID] = list[interface ...]
g_interf2APIDict = dict() #[interface] = list[api id...]
g_apiDict = dict() #[api id] = api object

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
    clusterID2InterfDict = dict()
    interf2APIDict = dict()
    apiDict = dict()

    with open(fileName,'r') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [clusterID, api, parameterstr, returnstr] = each
            if each[0] == 'clusterID':
                continue
            clusterID = int(clusterID)
            parameterSet = Trans2Set(parameterstr)
            returnSet = Trans2Set(returnstr)
            interface = GetInterf(api)
            if clusterID not in clusterID2InterfDict:
                clusterID2InterfDict[cluterID] = list()
            if interface not in interf2APIDict:
                interf2APIDict[interface] = list()
            oneObejct = APIObject(clusterID, interface, apiName, parameterSet, returnSet)
            apiDict[apiID] = oneObejct
            apiID += 1
            interf2APIDict[interface].append(apiID)
            clusterID2InterfDict[clusterID].append(interface)
    return clusterID2InterfDict, interf2APIDict, apiDict


def GetIntersect(apiID1, apiID2):
    global g_apiDict
    para_interset = g_apiDict[apiID1].parameterSet && g_apiDict[apiID2].parameterSet
    return_interset = g_apiDict[apiID1].returnSet && g_apiDict[apiID2].returnSet

    return para_interset, return_interset


def GetUnionset(apiID1, apiID2):
    return unionset


def GetFenmuWei(para_apiPairInterList, para_apiPairUnionList, return_apiPairInterList, return_apiPairUnionList):

def GetFenmuUnwei(para_apiPairInterList, para_apiPairUnionList, return_apiPairInterList, return_apiPairUnionList):


#measure the meg-level 's interface cohesion'
def Metric_msg_cohesion(interface):
    global g_interf2APIDict
    apiIDList = g_interf2APIDict[interface]
    if len(apiIDList) == 1:
        cohesion_wei = 1
        cohesion_unwei= 1
    else:
        from itertools import combinations
        apiIDPairList = list(combinations(apiIDList), 2)
        fenmu = len(apiIDPairList)  #perfect graph's edge number
        para_apiPairInterList = list()  # according to apiIDPairList
        para_apiPairUnionList = list()  # according to apiIDPairList
        return_apiPairInterList = list()  # according to apiIDPairList
        return_apiPairUnionList = list()  # according to apiIDPairList
        for apiPair in apiIDPairList:
            [para_interset, return_interset] = GetIntersect(apiPair[0], apiPair[1])
            [para_unionset, return_unionset] = GetUnionset(apiPair[0], apiPair[1])
            para_apiPairInterList.append(para_interset)
            para_apiPairUnionList.append(para_unionset)
            return_apiPairInterList.append(return_interset)
            return_apiPairUnionList.append(return_unionset)
            fenzi_weight = GetFenmuWei(para_apiPairInterList, para_apiPairUnionList, return_apiPairInterList, return_apiPairUnionList)
            fenzi_unweight = GetFenmuUnwei(para_apiPairInterList, para_apiPairUnionList, return_apiPairInterList, return_apiPairUnionList)

        cohesion_unwei = fenzi_unweight / float(fenmu)
        cohesion_wei = fenzi_weight / float(fenmu)

    return cohesion_wei, cohesion_unwei




if __name__ == '__main__':
    apiFileName = sys.argv[1]

    global g_interf2APIDict
    global g_clusterID2InterfDict
    global g_apiDict

    [g_clusterID2InterfDict, g_interf2APIDict, g_apiDict] = ReadAPIFile(apiFileName)
