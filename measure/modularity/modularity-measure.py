import sys
import config
import loaddata
import csv
import metric

def prepare(classfileName, calldepFile, concerndepFile):
    [classIDNameDict, classNameIDDict] = loaddata.loadClassList(classfileName)
    config.set_classidname_dict(classIDNameDict)
    config.set_classnameid_dict(classNameIDDict)

    classDepDict = loaddata.loadDepData(calldepFile, concerndepFile)
    config.set_classfinaldep_dict(classDepDict)
    print("load data end...")


def writeCSV(alist, filename):
    with open(filename, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)

def readClusterList(filename):
    fileList = list()
    with open(filename, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            clusterfilename = each[0]
            fileList.append(clusterfilename)
    return fileList

#reader clusterfile[contain, clusterid, classname], return indiv=[[classid1, classid2], []]
def getIndiv(clusterfilename):
    className2IDDict = config.get_classnameid_dict()
    indivDict = dict()  #dict[clusterID] = [classID]
    with open(clusterfilename, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [contain, clusterId, className] = each
            classId = className2IDDict[className]
            clusterId = int(clusterId)
            if clusterId not in indivDict:
                indivDict[clusterId] = list()
            indivDict[clusterId].append(classId)

    #from dict to list
    indiv = list()
    for clusterId in indivDict:
        indiv.append(indivDict[clusterId])
    return indiv


if __name__ == "__main__":
    classfileName = sys.argv[1]  #coverage releted
    calldepFile = sys.argv[2]    #coverage releted
    concerndepFile = sys.argv[3]
    fileListFile = sys.argv[4] #contains clusters whose metric will be computed
    outmeasureFile = sys.argv[5]
    fitness_method_list = config.GLOBAL_VAR_OBJECT.FITNESS_METHOD_LIST
    prepare(classfileName, calldepFile, concerndepFile)

    #read all cluster files, putput indivList
    clusterFileList = readClusterList(fileListFile)
    indivList = list() #this is consistent with clusterFileList
    for clusterfilename in clusterFileList:
        #indiv = [[id1, id2], [id4, id6], ...]
        indiv = getIndiv(clusterfilename)
        indivList.append(indiv)

    #compute the metrics of all candidates in indivList
    metric.computeFitnessThread(indivList, fitness_method_list)

    #compute metrics for each indiv
    measureList = list()
    for index in range(0, len(indivList)):
        indiv = indivList[index]
        clusterfilename = clusterFileList[index]
        [call_coh, call_coup, con_coh, con_coup] = metric.get_four_metrics(indiv)
        tmp =[clusterfilename, call_coh, call_coup, con_coh, con_coup]
        measureList.append(tmp)

    #write measures into file
    writeCSV(measureList, outmeasureFile)
