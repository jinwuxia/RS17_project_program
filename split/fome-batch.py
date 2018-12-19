import os
import subprocess
import sys
import csv


'''
usage:
python wca-or-limbo-batch.py
[project=]xwiki-plarform108
[method=]fome
[cluster_start=]2
[cluster_end=]50
[ioe-old_file=]ioe-measure_old.file
[ioe-new-file=]ioe-measure_new.file
> workflow-iof-measure.log

preapre files:
project.gitlog-projectcmt.csv
project.udb
project.xml
project_workflow_reduced.csv
project_testcase_name.csv
project_workflow_class.csv
'''

def genTSClustering_batch(project):
    datadir = "../testcase_data/"  + project + "/"
    reducedWorkflowFile = datadir + "workflow/" + project + "_workflow_reduced.csv"
    testcaseFile = datadir + "workflow/" + project + "_testcase_name.csv"
    includeClassFile = datadir + "workflow/" + project + "_workflow_reduced_class.csv"
    outTSClassFile =datadir + "coreprocess/" + project + "_testcase1_class.csv"
    outFvFile = datadir + "coreprocess/" + project + "_testcase1_fv.csv"
    cmd = "python  coreprocess/genTestCaseFv.py " + reducedWorkflowFile + " " +  testcaseFile + " null " + includeClassFile + " " +  outTSClassFile + " " + outFvFile
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)

    cmdlist = ["python", "coreprocess/testCaseClustering.py", outFvFile, 'null', 'jm', 'AVG', "1", project, 0.01]
    cmd = " ".join(cmdlist)
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)

    cmd = "mkdir " + datadir + "/testcaseClustering"
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)

    cmd = "mv " +  project+"_testcase1_jm_AVG*"  + "  " +  datadir + "/testcaseClustering/"
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)


def genMixDepForOverlapprocess_batch(project, cluster_start, cluster_end):
    datadir = "../testcase_data/"  + project + "/"
    xmlfile = datadir + "dependency/" + project + ".xml"
    xmlcsvfile = datadir + "dependency/" + project + "xml.csv"
    reducedWorkflowFile = datadir + "workflow/" + project + "_workflow_reduced.csv"
    comfile = datadir + "dependency/" + project + "com.csv"
    TSClassFile =datadir + "coreprocess/" + project + "_testcase1_class.csv"
    mixdepFile = datadir + "dependency/" + project + "_testcase1_mixedDep.csv"

    cmdlist = ["python", "dependency/xmlParser.py", xmlfile, xmlcsvfile]
    cmd = " ".join(cmdlist)
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)

    cmdlist = ["python", "dependency/comParser.py", reducedWorkflowFile, comfile]
    cmd = " ".join(cmdlist)
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)

    cmdlist = ["python", "dependency/mixParser.py", xmlcsvfile, "null", comfile, TSClassFile, mixdepFile]
    cmd = " ".join(cmdlist)
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)


def getFinalClusters_batch(project, cluster_start, cluster_end):
    datadir = "../testcase_data/"  + project + "/"
    fvFile = datadir + "coreprocess/" + project + "_testcase1_fv.csv"
    TSClassFile =datadir + "coreprocess/" + project + "_testcase1_class.csv"
    mixdepFile = datadir + "dependency/" + project + "_testcase1_mixedDep.csv"
    reducedWorkflowFile = datadir + "workflow/" + project + "_workflow_reduced.csv"
    metricFile = datadir + "coreprocess/" + project + "_fitness.csv"

    cmd = "mkdir " + datadir + "coreprocess/optionA-enum"
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)

    cmdlist = ["python", "coreprocess/optionA-enum/my_enum.py", datadir, fvFile, TSClassFile, mixdepFile, reducedWorkflowFile, cluster_start, cluster_end, metricFile]
    cmd = " ".join(cmdlist)
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)



def getOverlapClassCount(lapFileName):
    overlappedClassCount = 0
    with open(lapFileName, "r", newline="") as fp:
        reader = csv.reader(fp)
        overlappedClassCount = len(list(reader)) - 1
    return overlappedClassCount

#[clusterfile, apifile][...]
def getFileList(project, cluster_start, cluster_end):
    serv_list = range(cluster_start, cluster_end + 1) #xwiki108
    thr_list=[1,2,3, 4, 5,6, 7,8, 9,10] #if modify thr, we shoud change thr in my_enum.py
    thr_list = [ round(each/float(10), 1) for each in thr_list]
    datadir = "../testcase_data/"  + project + "/"
    reducedWorkflowFile = datadir + "workflow/" + project + "_workflow_reduced.csv"

    filelist = list()
    for service_count in serv_list:
        lapFileName = datadir + 'coreprocess/optionA-enum/' + project + '_testcase1_' + str(service_count) + '_class_lap.csv'
        overlappedClassCount = getOverlapClassCount(lapFileName)
        # has no overlap class, the next processes needed once
        if overlappedClassCount == 0:
            overlap_process_thr = round(0.1, 1)
            outClusterFileName  = datadir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            outClusterAPIFileName  = datadir + 'coreprocess/optionA-enum/' + project + '_testcase1_clustersAPI_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            filelist.append([outClusterFileName, outClusterAPIFileName])
            continue
        for thr in thr_list:
            overlap_process_thr = round(thr, 1)
            outClusterFileName  = datadir + 'coreprocess/optionA-enum/' + project + '_testcase1_clusters_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            outClusterAPIFileName  = datadir + 'coreprocess/optionA-enum/' + project + '_testcase1_clustersAPI_' + str(service_count) + '_' + str(overlap_process_thr) + '.csv'
            filelist.append([outClusterFileName, outClusterAPIFileName])
    return filelist

def getComponentAPI_batch(project, filelistfile):
    datadir = "../testcase_data/"  + project + "/"
    reducedWorkflowFile = datadir + "workflow/" + project + "_workflow_reduced.csv"
    cmd = "python coreprocess/getComponentProAPI.py " + reducedWorkflowFile + " " + filelistfile
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)


#step4: measure CHM and CHD metrics.
def measureCohesion_batch(project, filelist, method):
    datadir = "../testcase_data/"  + project + "/"
    #metric == 'private-dom':
    print("dom-cohesion measure start......")
    cmd1 = 'python ../measure/tosc-interf-dom-cohesion.py  '
    for each in filelist:
        clusterAPIFileName  = each[1]
        this_cmd = cmd1 + clusterAPIFileName + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)

    #metric == 'private-msg':
    print("msg-cohesion measure start......")
    cmd2 = 'python ../measure/tosc-interf-msg-cohesion.py '
    for each in filelist:
        clusterAPIFileName  = each[1]
        this_cmd = cmd2 + clusterAPIFileName + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)
    print("finish cohesion measurement batch")

def writecsv(alist, filename):
    with open(filename, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)



def measure_ioe_batch(project, method, filename, ioe_old_file, ioe_new_file):
    print("ioe measure start...")
    commitfile ='../testcase_data/' + project + '/dependency/' + project + "cmt.csv"
    cmd = "python ../measure/ioe-measure.py " + commitfile + " " + method + " " + filename + " " + ioe_old_file + " " + ioe_new_file
    returncode  = subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    project = sys.argv[1]
    alg = sys.argv[2] # #wca-uem, limb
    cluster_start = int(sys.argv[3])
    cluster_end = int(sys.argv[4])
    ioe_old_file = sys.argv[5]#detail value for each service
    ioe_new_file = sys.argv[6]#final value fot the system

    '''
    if project == 'jforum219':
        cluster_start = 16
        cluster_end = 47
    elif project == 'jpetstore6':
        cluster_start = 1
        cluster_end = 23
    elif project == 'roller520':
        cluster_start = 2
        cluster_end = 72
    elif project == 'xwiki-platform108':
        cluster_start = 50
        cluster_end = 200
    '''

    '''
    #step1: testcase clustering
    genTSClustering_batch(project)

    #step2: produce the mixdep for processing overlap
    genMixDepForOverlapprocess_batch(project, cluster_start, cluster_end)

    #step3: process overlap and generate final clusters and workflow-relevant metrics
    getFinalClusters_batch(project, cluster_start, cluster_end)
    '''

    filelist = getFileList(project, cluster_start, cluster_end)
    filelistfile = "../testcase_data/"  + project + "/coreprocess/" + project + "_beprocessedList.csv"
    writecsv(filelist, filelistfile)

    '''
    #step4:identify provided api
    getComponentAPI_batch(project, filelistfile)
    '''

    #step5: measure CHM and CHD metrics.
    measureCohesion_batch(project, filelist, alg)

    #step6:measure ioe
    measure_ioe_batch(project, alg, filelistfile, ioe_old_file, ioe_new_file)
    print("finish ioe measuremnt batch")
