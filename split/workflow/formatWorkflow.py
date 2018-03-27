import sys
import csv

def GetMethodName(strstr):
    methodName = ''
    tmp = strstr.split('(')[0]  #tmp=return methodname
    if ' ' in tmp:
        methodName = tmp.split()[1] # space, tab, \r
    else:
        methodName = tmp
    return methodName

def GetParaType(strstr):
    #print strstr
    strstr = strstr.split('(')
    #print 'strstr.split(()= ', strstr
    #print 'strstr[1]=', strstr[1]
    tmp = strstr[1]
    paraStr = tmp.split(')')[0]
    return paraStr

def GetReturnType(strstr):
    returnStr = ''
    tmp = strstr.split('(')[0]  #tmp=return methodname
    if ' ' in tmp:
        returnStr = tmp.split()[0] # space, tab, \r
    return returnStr

def GetClassName(methodName):
    arr = methodName.split('.')
    arr.pop(-1) #pop last element
    className = '.'.join(arr)
    return className

def ParseWorkflowFile(fileName):
    listList = list()
    with open(fileName) as fp:
        content = fp.readlines()
    lines = [line.strip('\n')  for line in content]
    traceID  = -1 #init
    lineNumber = 0
    while (lineNumber < len(lines)):
        line = lines[lineNumber]
        if line != '':
            if line.startswith('('):  #start with '(num)', a new trace
                print line
                traceID += 1
                orderID = 0

            else: #read two lines
                line1 = lines[lineNumber]
                lineNumber += 1
                line2 = lines[lineNumber]
                print line1
                print line2, '\n'
                method1 = GetMethodName(line1)
                m1_para = GetParaType(line1)
                m1_return = GetReturnType(line1)
                class1 = GetClassName(method1)
                method2 = GetMethodName(line2)
                m2_para = GetParaType(line2)
                m2_return = GetReturnType(line2)
                class2 = GetClassName(method2)

                oneList = [traceID, orderID, 'null', method1,method2, m1_para, m2_para, \
                          class1, class2, m1_return, m2_return]
                listList.append(oneList)
                orderID += 1

        lineNumber += 1
    return listList


def WriteCSV(fileName, listList):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerow(['traceID','order','structtype','method1','method2','m1_para', \
                         'm2_para','className1','className2','m1_return','m2_return'])
        writer.writerows(listList)
    print fileName


#format bvn13 plain workflow
if __name__ == '__main__':
    plainWorkflowFile = sys.argv[1]
    formatWorkflowFile = sys.argv[2]
    listList = ParseWorkflowFile(plainWorkflowFile)
    WriteCSV(formatWorkflowFile, listList)
