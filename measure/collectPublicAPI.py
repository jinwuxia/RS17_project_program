import sys
import csv
import understand

'''
from workflow file, collect public interface and api ,
generate  [interfaceclass, method, parameter, return]
'''
GLOBAL_INTERFACE_DICT = dict()#dict[interfaceclass] = [methodNameList]
USED_INTERFACE_DICT = dict() #dict[interfaceclass][methodName]= [paras, returns]
#filterStrList = ['com.raysmond.blog.controllers', 'com.raysmond.blog.admin.controllers', 'com.raysmond.blog.seo.controllers' ]
#filterStrList=['org.b3log.solo.processor']
#filterStrList=['org.apache.roller.weblogger.ui.rendering.servlets', 'org.apache.roller.weblogger.ui.struts2.ajax', 'org.apache.roller.weblogger.webservices.tagdata.TagDataServlet', 'org.apache.roller.weblogger.webservices.oauth']
#filterStrList=['fi.hut.soberit.agilefant.web']
filterStrList= [] #xwki
def isPublicInterface(className):
    if len(filterStrList) == 0:
        return True
    for filterStr in filterStrList:
        if className.startswith(filterStr):
            return True
    return False


def getInterfaceDetailFromUnd(undFile):
    interfaceDict = dict()  #dict[interfaceclass] = [methodNameList]
    #open database
    db = understand.open(undFile)
    classEntList = db.ents("public class ~unresolved ~unknown")
    interfaceEntList = db.ents("interface ~unresolved ~unknown")
    allEntList = classEntList
    allEntList.extend(interfaceEntList)
    print("ent len:", len(allEntList))
    for classent in allEntList:
        if classent.library() != "Standard":
            className = classent.longname()
            if isPublicInterface(className):
                print("interface Class", className)
                for methodent in classent.ents("Define", "method public member"):
                    if methodent.library() != "Standard":
                        methodName = methodent.longname()
                        print("interface Method", methodName)
                        if className not in interfaceDict:
                            interfaceDict[className] = list()
                        if methodName not in interfaceDict[className]:
                            interfaceDict[className].append(methodName)

    return interfaceDict



#use GLOBAL_INTERFACE_DICT,
def isInterface(className, startMethodName):
    if className in GLOBAL_INTERFACE_DICT:
        print("######class Y ", className)
        if startMethodName in GLOBAL_INTERFACE_DICT[className]:
            return True
        print("######method N", startMethodName)
    print('######class N', className)

    return False


#use, read and set USED_INTERFACE_DICT
#dict[interfaceclass][methodName]= [paras, returns]
def storeInterface(className, methodName, paras, returns):
    if className not in USED_INTERFACE_DICT:
        USED_INTERFACE_DICT[className] = dict()
    if methodName not in USED_INTERFACE_DICT[className]:
        USED_INTERFACE_DICT[className][methodName] = [paras, returns]


#set USED_INTERFACE_DICT
def getUsedAPIByWorkflowFile(fileName):
    with open(fileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            traceID = each[0]
            startMethodName = each[3]
            endMethodName = each[4]
            startMethodName = startMethodName.replace('#', '.')
            endMethodName = endMethodName.replace('#', '.')
            m1_para = each[5]
            m2_para = each[6]
            class1 = each[7]
            class2 = each[8]
            m1_return = each[9]
            m2_return = each[10]
            if traceID == 'traceID':
                continue
            if isInterface(class1, startMethodName):
                storeInterface(class1, startMethodName, m1_para, m1_return)
            if isInterface(class2, endMethodName):
                storeInterface(class2, endMethodName, m2_para, m2_return)


# store USED_INTERFACE_DICT into file
#dict[interfaceclass][methodName]= [paras, returns]
def getUsedAPIList():
    alist = list()
    for interface in USED_INTERFACE_DICT:
        for method in USED_INTERFACE_DICT[interface]:
            [paras, returns] = USED_INTERFACE_DICT[interface][method]
            tmp = [interface, method, paras, returns]
            alist.append(tmp)
    return alist

def writeCSV(alist, fileName):
    with open(fileName, "w", newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)
    print("write ", fileName, " end")


#python pro.py
#testcase_data/jpetstore/dependency/jpetstore.udb
#org.mybatis.jpetstore.web.actions
#testcase_data/jpetstore6/workflow/jpetstore6_workflow_reduced.csv
#testcase_data/jpetstpre6/workflow/jpetstore6_workflow_publicAPIdetail.csv
if __name__ == "__main__":
    undFile = sys.argv[1]
    #filterStr = sys.argv[2]  #filterstr is used to filter out interface class
    workflowFile = sys.argv[2]
    outInterfaceFile = sys.argv[3]  # it will be used to identify public intrerface for services

    # extract all interface and its public api from understand file by filtering
    GLOBAL_INTERFACE_DICT = getInterfaceDetailFromUnd(undFile)
    for classname in GLOBAL_INTERFACE_DICT:
        for methodName in GLOBAL_INTERFACE_DICT[classname]:
            pass
            #print ("und interface: ", classname, methodName)


    # generate USED_INTERFACE_DICT
    getUsedAPIByWorkflowFile(workflowFile)
    # store USED_INTERFACE_DICT into list
    apilist = getUsedAPIList()
    writeCSV(apilist, outInterfaceFile)
