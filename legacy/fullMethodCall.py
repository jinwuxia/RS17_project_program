import sys
import csv

def readCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp, delimiter = ';')
        for each in reader:
            resList.append(each)
    return resList

#methodName = returntype classname.methodname(paratype1,paratype2)
def getMethodName(methodName):
    tmp = methodName.split('(')[0].split(' ')[1]
    return tmp

def getClassName(methodName):
    tmp = methodName.split('(')[0].split(' ')[1]
    tmpList = tmp.split('.')
    tmpList.pop() #remove methodName
    className = '.'.join(tmpList)
    print methodName, 'xxx', className
    return className

def getReturnPara(methodName):
    returnType = ""
    para = ""
    
    returnType = methodName.split('(')[0].split(' ')[0]
    tmp = methodName.split('(') [1]   # ) or para,para)
    paraStrList = tmp.split(')')
    para = paraStrList[0]

    return returnType, para

def getFullMethodCall(methodCallList):
    fullList = list() #each=[methodName1, methodName2, method2return, method2para, className1, className2] 
    fullList.append(['method1', 'method2', 'method2return', 'method2para',  'class1', 'class2'])
    
    for each in methodCallList:
        iscross = 0
        [caller, callee] = each
        caller_class =  getClassName(caller)
        callee_class =  getClassName(callee)
        caller_method = getMethodName(caller)
        callee_method = getMethodName(callee)
        (callee_return, callee_para) = getReturnPara(callee)
        
        oneList = [caller_method, callee_method, callee_return, callee_para, caller_class, callee_class]
        fullList.append(oneList)


    return fullList


    
def writeCSV(fileName, resList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(resList)



#python fullMethodCall.py  methodCall.txt
#output allmethodCall.csv
if __name__ == "__main__":
    methodCallFileName = sys.argv[1]  #project_static_method_call.txt
    
    fullFileName = methodCallFileName.split('.txt')[0] + '_full.csv'
    print "output file: ", fullFileName, "\n"

    methodCallList = readCSV(methodCallFileName)
    fullCallList = getFullMethodCall(methodCallList)
    writeCSV(fullFileName, fullCallList)





