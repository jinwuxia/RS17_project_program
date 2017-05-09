import sys
import csv



def readCSV(fileName, filterStr):
    resList = list()
    classDict = dict()
    depsList = list()

    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp, delimiter = ',')
        for eachLine in reader:
            [fromClass, toClass, weight, fromNum, toNum] = eachLine
            if fromClass == "From Class":
                continue

            if fromClass.startswith(filterStr) == True and toClass.startswith(filterStr) == True:
                tmp = list([fromClass, toClass, int(weight)])
                resList.append(tmp)
                depsList.append(['depends', fromClass, toClass])

                if fromClass not in classDict:
                    classDict[fromClass] = 1
                if toClass not in classDict:
                    classDict[toClass] = 1
    fp.close()
    return resList, classDict, depsList


def mapNameID(classDict):
    name2ID = dict()
    ID2Name = dict()

    ID = 0

    for className in sorted(classDict.keys()):
        name2ID[className] = ID
        ID2Name[ID] = className
        ID += 1

    return name2ID, ID2Name 



def  genMatrix(depList, classSize, name2ID):
    featureVector = list() #list[1]= class1depsList

    # initialize an empty matrix
    for index in range(0, classSize):
        tmp = [0] * classSize #define a list with len = count
        featureVector.append(tmp)
    

    for each in depList:
        [fromClass, toClass, deps] = each
        fromID = -1
        toID = -1
        if fromClass in name2ID:
            fromID = name2ID[fromClass]
        else:
            print fromClass , " not in name2ID"
            continue

        if toClass in name2ID:
            toID = name2ID[toClass]
        else:
            print toClass, " not in name2ID"
            continue

        if fromID != -1 and toID != -1:
            featureVector[fromID][toID] = deps


    return featureVector

    
def write2CSV(fileName, ID2NameDict, fv):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        for index in range(0, len(ID2NameDict)):
            tmp = list()
            tmp.append(ID2NameDict[index]) # class name
            tmp.extend(fv[index])
            writer.writerow(tmp)
    fp.close()

def writersf(fileName, depsList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp, delimiter=' ')
        writer.writerows(depsList)
    fp.close()

#input und.csv; output class_dep.csv  class_dep.rsf
if __name__ == "__main__":
    undDepName = sys.argv[1]
    featureVectorName = sys.argv[2]
    rsfName = sys.argv[3]
    filterStr = sys.argv[4]
    [depList, classDict, rsfList] = readCSV(undDepName, filterStr)
    (name2IDDict, ID2NameDict) = mapNameID(classDict)
    fv = genMatrix(depList, len(classDict), name2IDDict)
    write2CSV(featureVectorName, ID2NameDict, fv)
    writersf(rsfName, rsfList)



                
