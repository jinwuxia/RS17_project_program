import sys
import csv

#classname -> classID
NAME2IDDict = dict()
ID2NAMEDict = dict()

#read struct_class_dep_marix, and get ClassDict, and matrix
def ReadMatrix(fileName):
    listlist = list()

    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        classID = 0
        for each in reader:
            className = each[0]
            NAME2IDDict[className] = classID
            ID2NAMEDict[classID] = className
            classID += 1
            del each[0]
            listlist.append(each)
    return listlist


def GetClassCount():
    return len(NAME2IDDict)


def GetClassID(className):
    ID = -1
    if className in NAME2IDDict:
        ID = NAME2IDDict[className]
    else:
        print "No found class: ", className
    return ID


def GetClassName(classID):
    return ID2NAMEDict[classID]


#read c1,c2,value into listlist
def ReadVector(fileName):
    listlist = list()
    for index in range(0, GetClassCount()):
        listlist.append( [0] * GetClassCount() )

    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            fromClass = each[0]
            toClass = each[1]
            deps = each[2]
            if fromClass == 'From Class':
                continue

            fromID = GetClassID(fromClass)
            toID = GetClassID(toClass)
            if fromID != -1 and toID != -1:
                listlist[fromID][toID] = deps
    return listlist

#to be filterd
def IsFilter(className, filterStr):
    if className.find(filterStr) != -1:
        return True
    else:
        return False

def WriteCSV(fileName, filterStr, list1, list2, list3, list4):
    print len(list1), ' ', len(list2), ' ', len(list3), ' ', len(list4)
    print fileName

    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['From Class', 'To Class', 'structDep', 'semanticSim', 'commuCost', 'workflowCurency'])
        for i in range(0, GetClassCount()):
            for j in range(0, GetClassCount()):
                if i != j and IsFilter(GetClassName(i), filterStr) == False and IsFilter(GetClassName(j), filterStr) == False:
                    each = [ GetClassName(i), GetClassName(j), list1[i][j], list2[i][j], list3[i][j], list4[i][j] ]
                    writer.writerow(each)


if __name__ == '__main__':
    structFileName = sys.argv[1]    #../RS17_source_data/RA17_jpetstore6/static/source/jpetstore_class_dep_fv.csv
    commucostFileName = sys.argv[2] #../RS17_source_data/RS17_jpetstore6/dynamic/source/jpetstore6_class_commu_deps.csv
    workflowFileName = sys.argv[3]  #../RS17_source_data/RS17_jpetstore6/dynamic/source/jpetstore6_class_workflow_deps.csv
    semanticFileName = sys.argv[4]  #../RS17_source_data/RS17_jpetstore6/semantic/source/jpetstore6_clas_domain_10_deps.csv
    filterStr = sys.argv[5]

    listS = ReadMatrix(structFileName)
    listW = ReadVector(workflowFileName)
    listM = ReadVector(commucostFileName)
    listC = ReadVector(semanticFileName)

    WriteCSV("jpetstore6_all_fv.csv", filterStr, listS, listC, listM, listW)
