import sys
import csv

ACTION2APIDict = dict() #[actionClass] = [api1 api2....]
CLUSTER2CLASSDict = dict() #[clusterID] =[actionclass ]

def GetAction(api):
    #interface name
    apiList = api.split('.')
    del apiList[len(apiList) - 1]
    actionClass = '.'.join(apiList)
    return actionClass


def ReadTsFile(fileName):
    action2APIDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [apiName] = each
            actionClass = GetAction(apiName)
            if actionClass not in action2APIDict:
                action2APIDict[actionClass] = list()
            action2APIDict[actionClass].append(apiName)
    return action2APIDict

def IsActionClass(className, PRE):
    if className.startswith(PRE):
        return True
    else:
        return False

def ReadClusterFile(fileName, PRE):
    cluster2ClassDict = dict()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [containes, clusterID, className] = each
            print each
            clusterID = int(clusterID)
            if clusterID not in cluster2ClassDict:
                cluster2ClassDict[clusterID] = list()
            if IsActionClass(className, PRE):
                cluster2ClassDict[clusterID].append(className)
    print cluster2ClassDict
    return cluster2ClassDict


def ExtractAPI():
    listlist = list()
    for clusterID in CLUSTER2CLASSDict:
        for actionClass in CLUSTER2CLASSDict[clusterID]:
            if actionClass in ACTION2APIDict:
                for api in ACTION2APIDict[actionClass]:
                    listlist.append([clusterID, '-1', api])
    return listlist

def WriteCSV(listlist, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)
    print fileName

#python pro.py tsFileName clusterFileName apiFileName  PRE
if __name__ == '__main__':
    tsFileName = sys.argv[1]
    clusterFileName = sys.argv[2]
    apiFileName = sys.argv[3]
    PRE = sys.argv[4] #PRE = 'org.mybatis.jpetstore.web.actions' #PRE = 'net.jforum.view.forum'

    ACTION2APIDict = ReadTsFile(tsFileName)
    #print ACTION2APIDict

    CLUSTER2CLASSDict = ReadClusterFile(clusterFileName, PRE)
    #print CLUSTER2CLASSDict

    apiList = ExtractAPI()
    print apiList
    WriteCSV(apiList, apiFileName)
