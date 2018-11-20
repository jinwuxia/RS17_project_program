'''
ananylze limbo,wca' class coverage
'''
import csv
import sys


def readClass(classFileName):
    classList = list()
    with open(classFileName, 'r', newline = "") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className] = each
            classList.append(className)
    return classList


def readCSV(rsfFileName, classList):
    classDict = dict()
    with open(rsfFileName, 'r', newline="") as fp:
        reader = csv.reader(fp, delimiter=' ')
        for each in reader:
            [dep, class1, class2] = each
            if class1 in classList and class2 in classList:
                if class1 not in classDict:
                    classDict[class1] = 1
                if class2 not in classDict:
                    classDict[class2] = 1
    print ('class number covered in wca/limbo=', len(classDict))
    print ('class coverage in wca/limbo= ', len(classDict)/len(classList))

classList =readClass(sys.argv[1])  #benchmark class, that is static classes "all_class.txt"
readCSV(sys.argv[2], classList)
