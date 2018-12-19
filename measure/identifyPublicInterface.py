import sys
import csv

APIdetailDict = dict()#dict[classname][methodname]=[paras, returns]
ClusterDict = dict() # ClusterDict[clusterId] = [className1, className2]

#generate APIdetailDict
#dict[classname][methodname]=[paras, returns]
def readAPIDetailFile(fileName):
    with open(fileName, "r", newline='') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className, methodName, paras, returns] = each
            if className not in APIdetailDict:
                APIdetailDict[className] = dict()
            if methodName not in APIdetailDict[className]:
                APIdetailDict[className][methodName] = [paras, returns]

#generate ClusterDict[clusterId] = [className1, className2]
def readClusterFile(fileName):
    with open(fileName, "r", newline='') as fp:
        reader = csv.reader(fp)
        for each in reader:
            #print(each)
            [contain, clusterId, className] = each
            if clusterId not in ClusterDict:
                ClusterDict[clusterId] = list()
            if className not in ClusterDict[clusterId]:
                ClusterDict[clusterId].append(className)


def writeCSV(alist, fileName):
    with open(fileName, "w", newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)
    #print("write ", fileName)

#input ClusterDict, APIdetailDict
#output [clusterID, interfacename]
def getPublicInterfaces():
    interfaceDict = dict() #dict[clusterId]=[inf1, inf2,]
    for clusterId in ClusterDict:
        interfaceDict[clusterId] = list()
        for className in ClusterDict[clusterId]:
            #className is a interface and not be recorded
            if className in APIdetailDict   and  className not in interfaceDict[clusterId]:
                interfaceDict[clusterId].append(className)

    #trans interfaceDict into list
    resList = list()
    for clusterId in interfaceDict:
        for className in interfaceDict[clusterId]:
            tmp = [clusterId, className]
            resList.append(tmp)
    return resList


#input publicInterfaceList, APIdetailDict[classname][methodname]=[paras, returns]
#output [clusterID, methodname]
def getPublicMethods(publicInterfaceList):
    resList = list()
    for each in publicInterfaceList:
        [clusterId, interfaceName] = each
        for methodName in APIdetailDict[interfaceName]:
            [paras, returns] = APIdetailDict[interfaceName][methodName]
            tmp = [clusterId, methodName, paras, returns]
            resList.append(tmp)
    return resList



if __name__ == "__main__":
    apidetailFile = sys.argv[1]
    clusterFile = sys.argv[2]
    outClusterInterfaceFile = sys.argv[3]
    outClusterAPIFile = sys.argv[4]


    readAPIDetailFile(apidetailFile)#generate APIdetailDict
    readClusterFile(clusterFile)#generate ClusterDict

    publicInterfaceList = getPublicInterfaces()
    writeCSV(publicInterfaceList, outClusterInterfaceFile)

    publicInterfaceMethodList = getPublicMethods(publicInterfaceList)
    writeCSV(publicInterfaceMethodList, outClusterAPIFile)
