import sys
import csv

DAO_PACKAGE='net.jforum.dao'
VIEW_PACKAGE='net.jforum.view'

ALL_CLASS_LIST = list() #className
TESTCASE_ALL_CLASS_LIST = list()
TESTCASE_1_CLASS_LIST = list()


def readCSV(fileName):
    oneList = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            if len(each) == 1:
                [className] = each
            else:  #len == 2
                [classID, className] = each
            oneList.append(className)
    return oneList

def countAllDaoViewClass(oneList):
    DAO_count = 0
    VIEW_count = 0
    for each in oneList:
        if each.startswith(DAO_PACKAGE):
            DAO_count += 1
        if each.startswith(VIEW_PACKAGE):
            VIEW_count += 1
    return DAO_count, VIEW_count

#use TESTCASE_1_CLASS_LIST, TESTCASE_ALL_CLASS_LIST
#commonclass = TESTCASE_ALL_CLASS_LIST - DAO - VIEW - TESTCASE_1_CLASS_LIST
def getTScommonClass():
    oneList = list()
    for className in TESTCASE_ALL_CLASS_LIST:
        if className.startswith(DAO_PACKAGE) == False and className.startswith(VIEW_PACKAGE) == False:
            if className not in TESTCASE_1_CLASS_LIST:
                oneList.append(className)
    return oneList


#use ALL_CLASS_LIST
#get tsNocoverClass = allclass- view - dao - testcase_allclass
def getNocoverClass():
    oneList = list()
    for className in ALL_CLASS_LIST:
        if className.startswith(DAO_PACKAGE) == False and className.startswith(VIEW_PACKAGE) == False:
            if className not in TESTCASE_ALL_CLASS_LIST:
                oneList.append(className)
    return oneList


def writeCSV(oneList, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        for each in oneList:
            writer.writerow([each])
    print fileName

#python pro.py   all_class.csv    testcase_all_class.csv   testcase1_class
#                out_ts_common.csv     out_no-cover.csv
if __name__  == '__main__':
    allClassFileName = sys.argv[1]
    testcaseClassFileName = sys.argv[2]
    testcase1classFileName = sys.argv[3]  #classes used for TS clustering
    tsCommonFileName = sys.argv[4]  #output
    nocoverFileName = sys.argv[5]   #output

    ALL_CLASS_LIST = readCSV(allClassFileName)
    TESTCASE_ALL_CLASS_LIST = readCSV(testcaseClassFileName)
    TESTCASE_1_CLASS_LIST = readCSV(testcase1classFileName)

    [dao_count, view_count] = countAllDaoViewClass(ALL_CLASS_LIST)

    #commonclass = TESTCASE_ALL_CLASS_LIST - DAO - VIEW - TESTCASE_1_CLASS_LIST
    ts_common_class_list = getTScommonClass()
    #get tsNocoverClass = allclass- view - dao - testcase_allclass
    nocover_class_list = getNocoverClass()

    writeCSV(ts_common_class_list, tsCommonFileName)
    writeCSV(nocover_class_list, nocoverFileName)

    print 'all_class', len(ALL_CLASS_LIST)
    print 'all_dao_class', dao_count
    print 'all_view_class', view_count
    print '\n'
    print 'ts_all_class', len(TESTCASE_ALL_CLASS_LIST)
    print 'ts_common_class', len(ts_common_class_list)
    print 'ts_core_class', len(TESTCASE_1_CLASS_LIST)

    print '\n'
    print 'nocover_class (not include Dao & view)', len(nocover_class_list), '\n'

    #nocover_class_list   and ts_common_class are our processing objects at next step.
