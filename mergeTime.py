import sys
import csv

totalCol = 10
method2IDDict = dict()
#ID2MethodDict = dict()
listlist = list()

def ReadCSV(filename):
    resList = list()
    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [methodID, methodName, className, meantime, stderr, paralen] = each
            method2IDDict[methodName] = methodID
            #ID2MethodDict[methodID] = methodName
            resList.append([methodID, methodName, className, meantime])
    return resList


def InitTable(oneList, colNum):
    n = len(method2IDDict)
    for i in range(0, n):
        tmpList = [0] * totalCol  #10 clolumn
        listlist.append(tmpList)

    for each in oneList:
        [methodID, methodName, className, meantime] = each
        ID = int(methodID)
        listlist[ID][0] = methodID
        listlist[ID][1] = methodName
        listlist[ID][2] = className
        listlist[ID][colNum] = meantime


def FillTableCol(filename, colNum):
    with open(filename, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [methodID, methodName, className, meantime, stderr, paralen] = each
            if methodName in method2IDDict:
                methodID = method2IDDict[methodName]
                ID = int(methodID)
                listlist[ID][colNum] = meantime
            else:
                print methodName

#fileName without dir
def ParseStr(fileName):
    tmp = fileName.split('.')[0]
    arr = tmp.split('_')
    test = arr[1]
    workload = arr[2]
    return test, int(int(workload)/10)

def WriteCSV(fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['ID', 'methodName', 'className', '10', '20', '30', '40', '50', '60', '70'])
        #writer.writerow(['ID', 'methodName', 'className', '10', '20', '30', '40'])
        writer.writerows(listlist)

#python mergetime.py  basctime.csv   time1.csv time2.csv .....
#just for jpetstore, need to be updated 
if __name__ == "__main__":
    basicFileName = sys.argv[1]
    otherFileNameList = [ sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7] ]

    basicList = ReadCSV(basicFileName)
    [test, workload] = ParseStr(basicFileName)
    InitTable(basicList, workload + 2) # first 3 col is "id, method, class"

    for eachFile in otherFileNameList:
        #print eachFile
        [test, workload] = ParseStr(eachFile)
        FillTableCol(eachFile, workload + 2)

    outFileName = "mergeTime_" + test + ".csv"
    print outFileName
    WriteCSV(outFileName)





