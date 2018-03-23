'''
delete duplicate workflow, and not-functional workflow
also generate testcase_name for final_workflow.
testcase_name is the service_method name like XXXAction.func1()
'''
import sys
import csv

#TESTCASE_PACKAGE_NAME = 'net.jforum.view'
#TESTCASE_PACKAGE_NAME = 'org.mybatis.jpetstore.web.actions'
#iNotDel aand reduceworklow function need to be care



def isIncluded(className, TESTCASE_PACKAGE_NAME):
    if className.startswith(TESTCASE_PACKAGE_NAME):
        return True
    else:
        return False


def isNotDel(methodName, className, TESTCASE_PACKAGE_NAME):
    filter_list = list()
    filter_list.append('BookmarkAction.process')
    filter_list.append('InstallAction.process')
    filter_list.append('LuceneStatsAction.process')
    filter_list.append('AdminAction.process')
    filter_list.append('AdminCommand.process')
    flag = True
    for each in filter_list:
        if each in methodName:
            flag = False
            break
    #OPTION:
    if methodName.endswith('<init>') == False and ('class$' not in methodName)  and isIncluded(className, TESTCASE_PACKAGE_NAME) and flag == True:
        return True
    else:
        return False


'''
judge this methodname 'view.method()' can stand for the testname name or not
beacause BookmarkAction.process()  InstallAction.process() are total entry, so they cannot be the testcasename
def isNotDel(methodName, className):
    #OPTION:
    if methodName.endswith('<init>') == False and ('class$' not in methodName)  and isIncluded(className):
        return True
    else:
        return False
'''

#resList[traceID] = [ [list1][list2][list3] ]
def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [traceID, order, structtype, method1, method2, m1_para, m2_para, className1, className2, m1_return, m2_return] = each
            if traceID == 'traceID':
                continue
            if order == '0':
                resList.append(list())
            oneList = [order, structtype, method1, method2, m1_para, m2_para, className1, className2, m1_return, m2_return]
            resList[int(traceID)].append(oneList)
    return resList




#if one trace is repetitive or not included in view, then delete this trace
def reduceWorkflow(initList, TESTCASE_PACKAGE_NAME):
    #print 'traceLen=', len(initList)
    resList = list()
    newID = 0
    methodID2NameDict = dict()
    methodDict = dict()  #dict[methodName] = traceID
    #judge this trace should be deleted or not
    for index in range(0, len(initList)):
        #print "\na new trace"
        isDel = True
        for eachList in initList[index]:
            [order, structtype, method1, method2, m1_para, m2_para, className1, className2, m1_return, m2_return] = eachList
            #OPTION:
            #if isNotDel(method2, className2, TESTCASE_PACKAGE_NAME):
            if isNotDel(method1, className1, TESTCASE_PACKAGE_NAME):
                isDel = False
                #OPTION:
                #oneStr = method2
                oneStr = method1
                #print oneStr
                break  #break the loop, use the fisrt found name as testcaseName

        if isDel == False:
            #ignore the duplicate and ;
            if oneStr not in methodDict:
                methodID2NameDict[newID] = oneStr
                methodDict[oneStr] = newID
                print 'traceID=', newID, 'traceName=', oneStr
                #save this trace
                resList.append(list())
                for eachList in initList[index]:
                    resList[newID].append(eachList)
                newID += 1
            else: #duplicate, repalce with longer oneStr
                oldTraceID = methodDict[oneStr]
                oldTraceLen= len(resList[oldTraceID])
                if oldTraceLen < len(initList[index]):
                    print 'repalce_traceID=', oldTraceID, 'traceName=', oneStr
                    resList[oldTraceID] = list()
                    for eachList in initList[index]:
                        resList[oldTraceID].append(eachList)
    return resList, methodID2NameDict


def writeCSV(aList, fileName):
    resList = list()
    resList.append(['traceID', 'order', 'structtype', 'method1', 'method2', 'm1_para', 'm2_para', 'className1', 'className2', 'm1_return', 'm2_return'])
    for traceID in range(0, len(aList)):
        for oneList in aList[traceID]:
            tmpList = [traceID]
            tmpList.extend(oneList)
            resList.append(tmpList)
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)
    print fileName

def writeTestCase(aDict, fileName):
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        for ID in aDict:
            writer.writerow([aDict[ID]])
    print fileName

#python pro.py workflowfile.csv  outputworkflowReducedworkflow.csv   outputtestcaseFileName.csv  org.b3log.solo
if __name__ == "__main__":
    workflowFileName = sys.argv[1]
    reducedWorkflowFileName = sys.argv[2]
    testcaseFileName = sys.argv[3]
    TESTCASE_PACKAGE_NAME = sys.argv[4]

    initList = readCSV(workflowFileName)
    #resList is the reduced workflowList;  methodID2NameDict is the traceID2TraceName
    (resList, methodID2NameDict) = reduceWorkflow(initList, TESTCASE_PACKAGE_NAME)
    #save the reduced workflowList
    writeCSV(resList, reducedWorkflowFileName)
    #save the testcaseName
    writeTestCase(methodID2NameDict, testcaseFileName)
