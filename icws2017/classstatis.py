#ananylze icws' class coverage
import csv
import sys
def readClass(classFileName):
    classList = list()
    with open(classFileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classList.append(className)
    return classList

def readCSV(rsfFileName):
    relationList = list()
    with open(rsfFileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [class1, class2, weight] = each
            weight = float(weight)
            relationList.append([class1, class2, weight])
    return relationList

def statisClassByThr(relationList, allClassList, thr):
    weightList = list()  #[ class1, class2,...], < weight's class
    for each in relationList:
        [class1, class2, weight] = each
        if weight >= thr and class1 in allClassList and class2 in allClassList:
            if class1 not in weightList:
                weightList.append(class1)
            if class2 not in weightList:
                weightList.append(class2)
    return weightList

def statisAll(relationList, allClassList):
    resultDict = dict()   #[weight] = classList
    for thr in range(0, 11):  #[1,2,3,4,5,...10]
        thr = round(thr/float(10), 1)
        oneClassList = statisClassByThr(relationList, allClassList, thr)
        resultDict[thr] = oneClassList
        print (str(thr) + ',' + str(len(oneClassList)))

allClassList = readClass(sys.argv[1]) #all_class.txt
relationList = readCSV(sys.argv[2]) #icws synsim.csv
statisAll(relationList, allClassList)
