import sys
import csv

def readCSV(fileName, filterStr):
    depsList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp, delimiter = ',')
        for eachLine in reader:
            [fromClass, toClass, weight, fromNum, toNum] = eachLine
            if fromClass == "From Class":
                continue

            if fromClass.startswith(filterStr) == True and toClass.startswith(filterStr) == True:
                depsList.append(['depends', fromClass, toClass])
    return depsList


def writersf(fileName, depsList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp, delimiter=' ')
        writer.writerows(depsList)
    fp.close()

#python pro.py   und.csv   class_dep.rsf  packagename
if __name__ == "__main__":
    undDepName = sys.argv[1]
    rsfName = sys.argv[2]
    filterStr = sys.argv[3]
    rsfList = readCSV(undDepName, filterStr)
    writersf(rsfName, rsfList)
