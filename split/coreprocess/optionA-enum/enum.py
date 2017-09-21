# -*- coding: utf-8 -*
class EstimationObject:
    def __init__(self, ts, thr, fitness):
        self.ts = ts #core service count
        self.thr = thr
        self.fitness = fitness

project               = 'jforum219'
data_dir              = "../../../testcase_data/jforum219_1/"
featureVectorFileName = data_dir + 'coreprocess/' + project + '_testcase1_fv.csv'
classFileName         = data_dir + 'coreprocess/' + project + '_testcase1_class.csv'
depFileName          = data_dir + 'dependency/' + project + '_testcase1_mixedDep.csv'
traceDepFileName     = data_dir + 'dependency/' + project + '_testcase1_traceDep.csv'
workflowFileName     = data_dir + 'workflow/' + project + '_workflow_reduced.csv'


#when service = service_count,compute the clusters metric
def metric_analyzeCluster(tsclusterFileName):
    global featureVectorFileName
    global classFileName
    import analyzeAllCluster_f as moduleA
    [nonOverlappedClassCount,  nonOverlappedAvg, \
    overlappedClassCount, overlappedAvg, \
    high_overlappedClassCount, high_overlappedAvg,\
    low_overlappedClassCount, low_overlappedAvg] = moduleA.analyzeOneCluster(tsclusterFileName, featureVectorFileName, classFileName)

    return nonOverlappedClassCount,  nonOverlappedAvg, \
    overlappedClassCount, overlappedAvg, \
    high_overlappedClassCount, high_overlappedAvg,\
    low_overlappedClassCount, low_overlappedAvg


#when service = service_count,generate three files for next processing
def analyzeCluster(tsclusterFileName, nonlapFileName, lapFileName, mergedFvFileName):
    global featureVectorFileName
    global classFileName
    import analyzeOneCluster_f as moduleB
    #generate file
    moduleB.analyzeOneCluster(tsclusterFileName, featureVectorFileName, classFileName, nonlapFileName, lapFileName, mergedFvFileName)


#when service = service_count, thr = overlap_process_thr,  process the overlapped class, generate file
def processOverlap(overlap_process_thr, tsclusterFileName, nonlapFileName, lapFileName, outClusterFileName):
    global depFileName
    global traceDepFileName
    import processOverlappedClass_f as moduleC
    moduleC.processOverlappedClass(depFileName, traceDepFileName, tsclusterFileName, nonlapFileName, lapFileName, outClusterFileName, overlap_process_thr)

#when service = service_count, thr = overlap_process_thr, analyze the metric
def metric_processOverlap(tsclusterFileName, outClusterFileName):
    global workflowFileName
    import analyzeProcessOverlapRes_f as moduleD
    metricList = moduleD.analyzeProcessOverlapRes(outClusterFileName, tsclusterFileName, workflowFileName)
    [totalClusterNum, noZeroClusterNum, repeatClassNum, repeatClassAvg, \
    interComWfCount, withinComWfCount, interCallCount, interCallCount_avg, \
    interCallCount_f, interCallCount_avg_f, APICount, APICount_avg]           = metricList
    return metricList


def writeCSV(aList, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(aList)
    print fileName

def processNextStep(overlap_process_thr, tsclusterFileName, lapFileName, nonlapFileName, mergedFvFileName, outClusterFileName):
    analyzeCluster(tsclusterFileName, nonlapFileName, lapFileName, mergedFvFileName)  #gen last three files

    processOverlap(overlap_process_thr, tsclusterFileName, nonlapFileName, lapFileName, outClusterFileName)  #gen  outClusterFileName

    [totalClusterNum, noZeroClusterNum, repeatClassNum, repeatClassAvg, \
    interComWfCount, withinComWfCount, interCallCount, interCallCount_avg, \
    interCallCount_f, interCallCount_avg_f, APICount, APICount_avg] \
    = metric_processOverlap(tsclusterFileName, outClusterFileName)

    oneList = list()
    oneList.append(noZeroClusterNum)
    oneList.extend([repeatClassNum, repeatClassAvg])
    oneList.extend([interComWfCount, withinComWfCount, interCallCount, interCallCount_avg])
    oneList.extend([interCallCount_f, interCallCount_avg_f, APICount, APICount_avg])
    #fitness = 0.5 * (interComWfCount - withinComWfCount) + 0.5 * repeatClassNum
    #oneList.append(fitness)
    return oneList


#compare tow list is equal or not
def isEqualList(list1, list2):
    if len(list1) != len(list2):
        return False

    diffList = [ abs(list1[index] - list2[index])    for index in range(0, len(list1)) ]
    if sum(diffList) <= 0.00001:
        return True

    return False

if __name__ == '__main__':
    global data_dir
    global project
    global featureVectorFileName
    global classFileName
    global depFileName
    global traceDepFileName
    global workflowFileName
    project               = 'jforum219'
    data_dir              = "../../../testcase_data/jforum219_1/"
    featureVectorFileName = data_dir + 'coreprocess/' + project + '_testcase1_fv.csv'
    classFileName         = data_dir + 'coreprocess/' + project + '_testcase1_class.csv'
    depFileName           = data_dir + 'dependency/' + project + '_testcase1_mixedDep.csv'
    traceDepFileName      = data_dir + 'dependency/' + project + '_testcase1_traceDep.csv'
    workflowFileName      = data_dir + 'workflow/' + project + '_workflow_reduced.csv'

    serv_list = range(16, 48)
    thr_list = range(1, 101)
    thr_list = [ round(each/float(100), 2) for each in thr_list]
    resList = list() #[0] = [TS, thr]

    for service_count in serv_list:
        tsclusterFileName = data_dir + 'coreprocess/testcaseClustering/' + project + '_testcase1_jm_AVG_' + str(service_count) + '.csv'
        lapFileName       = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_class_lap.csv'
        nonlapFileName    = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_class_nolap.csv'
        mergedFvFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_classclusterFv.csv'
        '''
        [nonOverlappedClassCount,  nonOverlappedAvg, \
        overlappedClassCount, overlappedAvg, \
        high_overlappedClassCount, high_overlappedAvg,\
        low_overlappedClassCount, low_overlappedAvg]    = metric_analyzeCluster(tsclusterFileName)
        '''
        clusterMetricList = metric_analyzeCluster(tsclusterFileName)
        [nonOverlappedClassCount,  nonOverlappedAvg, \
        overlappedClassCount, overlappedAvg, \
        high_overlappedClassCount, high_overlappedAvg,\
        low_overlappedClassCount, low_overlappedAvg] = clusterMetricList
        # has no overlap class, the next processes needed once
        if overlappedClassCount == 0:
            overlap_process_thr = round(0.01, 2)
            outClusterFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            lapResMetricList = processNextStep(overlap_process_thr, tsclusterFileName, lapFileName, nonlapFileName, mergedFvFileName, outClusterFileName)
            oneList = list()
            oneList.append(service_count)
            oneList.append(overlap_process_thr)
            oneList.extend(clusterMetricList)
            oneList.extend(lapResMetricList)
            resList.append(oneList)
            print oneList
            continue
        preList = list()
        for thr in thr_list:
            overlap_process_thr = round(thr, 2)
            outClusterFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            lapResMetricList = processNextStep(overlap_process_thr, tsclusterFileName, lapFileName, nonlapFileName, mergedFvFileName, outClusterFileName)
            if isEqualList(preList, lapResMetricList) == False:
                oneList = list()
                oneList.append(service_count)
                oneList.append(overlap_process_thr)
                oneList.extend(clusterMetricList)
                oneList.extend(lapResMetricList)
                resList.append(oneList)
                print oneList
                preList = [copyValue for copyValue in lapResMetricList]

    fileName = sys.argv[1]
    writeCSV(resList, fileName)
