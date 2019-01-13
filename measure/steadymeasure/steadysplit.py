import sys
import csv


#bench_serviceDict[className] = serviceID
def readBenchmarkService(filename):
    bench_serviceDict = dict()  #class->serviceID
    with open(filename, 'r', newline='') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, serviceID, className] = each
            bench_serviceDict[className] = serviceID
    return bench_serviceDict

#clusterDict[clusterID] =[classname ]
def readCluster(filename):
    clusterDict = dict()
    with open(filename, 'r', newline='') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, serviceID, className] = each
            if serviceID not in clusterDict:
                clusterDict[serviceID] = list()
            clusterDict[serviceID].append(className)
    return clusterDict


def countThechange(clusterDict, benchDict):
    speadServiceDict = dict()  #res[clusterID][benchserviceID] = [classname]
    for clusterID in clusterDict:
        if clusterID not in speadServiceDict:
            speadServiceDict[clusterID] = dict()
        for className in clusterDict[clusterID]:
            benserviceID = benchDict[className]
            if benserviceID not in speadServiceDict[clusterID]:
                speadServiceDict[clusterID][benserviceID] = list()
            speadServiceDict[clusterID][benserviceID].append(className)
    return speadServiceDict


def measure(speadServiceDict, clusterDict):
    measureList = list()
    measureList.append(['clusterID', 'clusterSize', 'spreadservicecount', 'maxsizeinaservice', 'detail'])
    for clusterID in speadServiceDict:
        clusterSize = len(clusterDict[clusterID])
        differentserviceCount = len(list(speadServiceDict[clusterID].keys()))
        sameserviceCountList = list()
        for serviceID in speadServiceDict[clusterID]:
            count = len(speadServiceDict[clusterID][serviceID])
            sameserviceCountList.append(count)
        sameserviceCountList.sort(reverse = True)
        maxSize = sameserviceCountList[0]
        #print (sameserviceCountList)
        for index in range(0, len(sameserviceCountList)):
            sameserviceCountList[index] = str(sameserviceCountList[index])
        strstr = ';'.join(sameserviceCountList)

        tmp = [clusterID, clusterSize, differentserviceCount, maxSize, strstr]
        measureList.append(tmp)
    return measureList



if __name__ == "__main__":
    benFile = sys.argv[1]
    clusterFile = sys.argv[2]
    bench_serviceDict = readBenchmarkService(benFile)
    #print (bench_serviceDict)
    clusterDict = readCluster(clusterFile)
    #print(clusterDict)
    speadServiceDict = countThechange(clusterDict, bench_serviceDict)
    print(speadServiceDict)
    listlist = measure(speadServiceDict, clusterDict)
    for each in listlist:
        if each[0] == "clusterID":
            continue
        print (each[3] / float(each[1]))
        tmp = [str(eachone) for eachone in each]
        #strstr = ','.join(tmp)
        #print (strstr)
