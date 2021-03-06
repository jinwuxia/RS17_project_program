import sys
import csv


'''
normalized tarcedep using  testcase1_20_classclusterFv
'''

#fileName = 'testcase1_20_classclusterFv'
def readTraceDepFile(fileName):
    trace_dep_dict = dict()  #dict[classNAme][clusterID] = dep
    with open(fileName, 'r', newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [className, clusterID, count] = each
            if className == 'className':
                continue
            clusterID = int(clusterID)
            count = int(count)
            if className not in trace_dep_dict:
                trace_dep_dict[className] = dict()
            trace_dep_dict[className][clusterID] = count
    return trace_dep_dict

def normalized(dep_dict, FENWEI_THR):
    tmpList =list()
    for className in dep_dict:
        for clusterID in dep_dict[className]:
            tmpList.append(dep_dict[className][clusterID])
    #normalized
    sortedList = sorted(tmpList)
    fenweiIndex = int( len(tmpList) * FENWEI_THR)
    maxValue = sortedList[fenweiIndex]
    minValue = min(tmpList)

    for className in dep_dict:
        for clusterID in dep_dict[className]:
            if dep_dict[className][clusterID] > maxValue:
                dep_dict[className][clusterID] = maxValue
            dep_dict[className][clusterID] = (dep_dict[className][clusterID] - minValue) / float(maxValue - minValue)
    return dep_dict



def writeCSV(dep_dict, outfileName):
    resList = list()
    for className in dep_dict:
        for clusterID in dep_dict[className]:
            resList.append([className, clusterID, round(dep_dict[className][clusterID], 5)])
    with open(outfileName, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(['className', 'clusterID', 'tracedep'])
        writer.writerows(resList)
    print (outfileName)


#fileName is classclusterFv.csv
#outfilename is tracedep
def traceParser(fileName, outfileName):
    FENWEI_THR = 0.9
    dep_dict = readTraceDepFile(fileName)
    dep_dict = normalized(dep_dict, FENWEI_THR)
    writeCSV(dep_dict, outfileName)
