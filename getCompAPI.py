import sys
import csv

def readCSV2Dict(fileName):
    class2compDict = dict()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for eachLine in reader:
            [componentID, className] = eachLine
            class2compDict[className] = componentID
    return class2compDict

def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [method1, method2, method2return, method2para, class1, class2] = each
            if method1 == 'method1':
                continue
            resList.append(each)
    return resList


# for the method class not in component, then set compID = -1
def getCompAPI(methodCallList, class2compDict):
    APIList = list() #each=[comp2, method2, returntype, para]
    APIList.append(['component', 'method', 'returntype', 'paralist'])
    
    for each in methodCallList:
        iscross = 0
        caller_comp = '-1'
        callee_comp = '-1'
        [caller_method, callee_method, callee_return, callee_para, caller_class, callee_class] = each
        if caller_class in class2compDict:
            caller_comp = class2compDict[caller_class]
        if callee_class in class2compDict:
            callee_comp = class2compDict[callee_class]
        
        if callee_comp != -1 and callee_comp != caller_comp:
            iscross = 1 
        else:
            iscross = 0
        
        if iscross == 1:
            APIList.append([callee_comp, callee_method, callee_return, callee_para])

    return  APIList


    
def writeCSV(fileName, resList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)



#python extractCompAPI.py  methodCall.txt  clusterFileName.txt
#output   compAPI.csv
if __name__ == "__main__":
    methodCallFileName = sys.argv[1]  #project_code_method_call_full.txt
    clusterFileName = sys.argv[2]     #../../static/partitionCluster/project_cluster_FV_DIST_MERGE_CLUSTERNUM.csv
    
    apitype = methodCallFileName.split('/')[len(methodCallFileName.split('/')) - 1].split('_')[1]
    tmp = clusterFileName.split('/')
    clustername = tmp.pop()
    clustername = clustername.split('.csv')[0]
    clusterdir = tmp.pop()
    compAPIFileName = '/'.join(tmp) + '/partitionApi/' + clustername + '_' + apitype + '_api.csv' 
   

    class2compDict = readCSV2Dict(clusterFileName)
    methodCallList = readCSV(methodCallFileName)
    (APIList) = getCompAPI(methodCallList, class2compDict)

    writeCSV(compAPIFileName, APIList)




