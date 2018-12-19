# -*- coding: utf-8 -*
import sys
import csv
import subprocess

project               = sys.argv[1] #'xwiki-platform108'
data_dir              = sys.argv[2]#"../../../testcase_data/xwiki-platform108/
featureVectorFileName = sys.argv[3]#data_dir + 'coreprocess/' + project + '_testcase1_fv.csv'
classFileName         = sys.argv[4]#data_dir + 'coreprocess/' + project + '_testcase1_class.csv'
depFileName          = sys.argv[5]#data_dir + 'dependency/' + project + '_testcase1_mixedDep.csv'
workflowFileName     = sys.argv[6]#data_dir + 'workflow/' + project + '_workflow_reduced.csv'
clusternum_start     = sys.argv[7]
clusternum_end       = sys.argv[8]
MetricFileName       = sys.argv[9] #fitness file
class EstimationObject:
    def __init__(self, ts, thr, fitness):
        self.ts = ts #core service count
        self.thr = thr
        self.fitness = fitness

#when service = service_count,compute the clusters metric
def metric_analyzeCluster(tsclusterFileName):
    global featureVectorFileName
    global classFileName
    import analyzeAllCluster_f as moduleA
    resList =  moduleA.analyzeOneCluster(tsclusterFileName, featureVectorFileName, classFileName)
    '''
    return nonOverlappedClassCount,  nonOverlappedAvg, \
    overlappedClassCount, overlappedAvg, \
    high_overlappedClassCount, high_overlappedAvg,\
    low_overlappedClassCount, low_overlappedAvg
    '''
    return resList



#when service = service_count,generate four files for next processing
def analyzeCluster(tsclusterFileName, nonlapFileName, lapFileName, mergedFvFileName, traceDepFileName, benchClusterFileName):
    global featureVectorFileName
    global classFileName
    import analyzeOneCluster_f as moduleB
    import traceParser_f  as moduleBB
    #generate file
    moduleB.analyzeOneCluster(tsclusterFileName, featureVectorFileName, classFileName, nonlapFileName, lapFileName, mergedFvFileName, benchClusterFileName)
    moduleBB.traceParser(mergedFvFileName, traceDepFileName)

#when service = service_count, thr = overlap_process_thr,  process the overlapped class, generate file
def processOverlap(overlap_process_thr, tsclusterFileName, nonlapFileName, lapFileName, traceDepFileName,  outClusterFileName):
    global depFileName
    import processOverlappedClass_f as moduleC
    moduleC.processOverlappedClass(depFileName, traceDepFileName, tsclusterFileName, nonlapFileName, lapFileName, outClusterFileName, overlap_process_thr)

#when service = service_count, thr = overlap_process_thr, analyze the metric
def metric_processOverlap(tsclusterFileName, outClusterFileName):
    global workflowFileName
    import analyzeProcessOverlapRes_f as moduleD
    metricList = moduleD.analyzeProcessOverlapRes(outClusterFileName, tsclusterFileName, workflowFileName)
    '''
    [totalClusterNum, noZeroClusterNum, repeatClassNum, repeatClassAvg, \
    interComWfCount, withinComWfCount, interCallCount, interCallCount_avg, \
    interCallCount_f, interCallCount_avg_f, APICount, APICount_avg]           = metricList
    '''
    return metricList


def writeCSV(aList, fileName):
    with open(fileName, 'w',newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(aList)
    print (fileName)


#compare tow list is equal or not
def isEqualList(list1, list2):
    if len(list1) != len(list2):
        return False

    diffList = [ abs(list1[index] - list2[index])    for index in range(0, len(list1)) ]
    if sum(diffList) <= 0.00001:
        return True

    return False



def getOverlapClassCount(lapFileName):
    overlappedClassCount = 0
    with open(lapFileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        overlappedClassCount = len(list(reader)) - 1

    return overlappedClassCount

#generate outClusterFileName: _servenum_thr_cluster.csv
def produceFinalClusterFiles():
    serv_list = range(clusternum_start,clusternum_end + 1) #xwiki108
    #serv_list = range(2,71)#solo270
    #serv_list = range(1,27) #bvn13
    #serv_list = range(7, 73)  #roler520
    #serv_list = range(16, 48) #jforum219
    #serv_list = range(1, 11)  #jpetstore
    #thr_list = range(1, 11)
    thr_list=[1,2, 3,4, 5,6, 7,8, 9,10]
    thr_list = [ round(each/float(10), 1) for each in thr_list]
    resList = list() #[0] = [TS, thr]

    for service_count in serv_list:
        tsclusterFileName = data_dir + 'coreprocess/testcaseClustering/' + project + '_testcase1_jm_AVG_' + str(service_count) + '.csv'
        lapFileName       = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_class_lap.csv'
        nonlapFileName    = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_class_nolap.csv'
        mergedFvFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_classclusterFv.csv'
        traceDepFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_traceDep.csv'
        benchClusterFileName = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_benchCluster.csv'

        #this step is not related with thrprocess cluster from testcase clustering, get overlap, nonlap, benchclusters, etc.
        analyzeCluster(tsclusterFileName, nonlapFileName, lapFileName, mergedFvFileName, traceDepFileName, benchClusterFileName)  #gen last 4 files
        # has no overlap class, the next processes needed once
        overlappedClassCount = getOverlapClassCount(lapFileName)
        if overlappedClassCount == 0:
            overlap_process_thr = round(0.1, 1)
            outClusterFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            #process overlap, this step is related to thr.
            processOverlap(overlap_process_thr, tsclusterFileName, nonlapFileName, lapFileName, traceDepFileName, outClusterFileName)  #gen  outClusterFileName
            continue
        for thr in thr_list:
            overlap_process_thr = round(thr, 1)
            outClusterFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            processOverlap(overlap_process_thr, tsclusterFileName, nonlapFileName, lapFileName, traceDepFileName, outClusterFileName)  #gen  outClusterFileName



def finalMetric():
    serv_list = range(clusternum_start,clusternum_end + 1) #xwiki108
    thr_list=[1,2,3, 4, 5,6, 7,8, 9,10]
    thr_list = [ round(each/float(10), 1) for each in thr_list]
    resList = list() #[0] = [TS, thr]

    for service_count in serv_list:
        tsclusterFileName = data_dir + 'coreprocess/testcaseClustering/' + project + '_testcase1_jm_AVG_' + str(service_count) + '.csv'
        lapFileName       = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_class_lap.csv'

        overlappedClassCount = getOverlapClassCount(lapFileName)
        # has no overlap class, the next processes needed once
        if overlappedClassCount == 0:
            overlap_process_thr = round(0.1, 1)
            outClusterFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            #when service = service_count, thr = overlap_process_thr, analyze the metric such as interwf, apinum
            lapResMetricList = metric_processOverlap(tsclusterFileName, outClusterFileName)
            oneList = list()
            oneList.append(service_count)
            oneList.append(overlap_process_thr)
            oneList.extend(lapResMetricList)
            resList.append(oneList)
            print (oneList)
            continue
        for thr in thr_list:
            overlap_process_thr = round(thr, 1)
            outClusterFileName  = data_dir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            lapResMetricList = metric_processOverlap(tsclusterFileName, outClusterFileName)
            oneList = list()
            oneList.append(service_count)
            oneList.append(overlap_process_thr)
            oneList.extend(lapResMetricList)
            resList.append(oneList)
            print(oneList)
    writeCSV(resList, MetricFileName)


if __name__ == "__main__":

    #step 1: batch process all cases, generate final cluter files after overlap processing
    produceFinalClusterFiles()

    #step2: batch process all final clusterf files, generate metrics
    finalMetric()
    
    #step3: batch process all , generate api for each clusters.
    getComponentAPI_batch()
