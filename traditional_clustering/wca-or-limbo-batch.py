import os
import subprocess
import sys
import csv

'''
usage:
python wca-or-limbo-batch.py
[project=]xwiki-plarform108
[method=]limbo, or wca-uem
[filter=]all
[ioe-old_file=]ioe-measure_old.file
[ioe-new-file=]ioe-measure_new.file
> workflow-iof-measure.log

the prepared file include:
data/project/traditional_clustering/
data/project/traditional_clustering/$project$-$method$/*  need produce all cluster files by arcade.jar
data/project/traditional_clustering/$project$-$method$-filter-$filter$/
../testcase-data/project/workflow/project_workflow_reduced.csv
filterclassfile= data/project/traditional_clustering/$project$_testcase_$filter$_class.csv
'''

#step1: filter the clusters by using tescase class benchmark
def filter_batch(filter, project, servnum_start, servnum_end, method):
    #filter = "all"
    benchmark_class_filename = "../testcase_data/" + project + "/traditional_clustering/" + project + "_testcase_" + filter +"_class.csv"
    for clusternum in range(servnum_start, servnum_end):
        after_filter_cluster_filename =  "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_cluster_" + str(clusternum) + ".csv"
        if method == "wca-uem":
            before_filter_cluster_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "/jwx_wca_uem_WCA_preselected_uem_"+ str(clusternum) + "_clusters.rsf.csv"
        elif method == "limbo":
            before_filter_cluster_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "/jwx_limbo_ilm_LIMBO_preselected_ilm_"+ str(clusternum) + "_clusters.rsf.csv"
        filterCmd  = "python filterOutCluster.py " + benchmark_class_filename +  " " + before_filter_cluster_filename + " " + after_filter_cluster_filename
        returncode  = subprocess.call(filterCmd, shell=True)


def genFilelistFile(filter, project,servnum_start, servnum_end, method, filename):
    alist=list()
    for clusternum in range(servnum_start, servnum_end+1):
        after_filter_cluster_filename =  "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_cluster_" + str(clusternum) + ".csv"
        after_filter_pub_inf_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_pub_inf"  + str(clusternum) + '.csv'
        after_filter_pub_api_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_pub_api"  + str(clusternum) + '.csv'
        after_filter_pri_inf_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_pri_inf"  + str(clusternum) + '.csv'
        after_filter_pri_api_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_pri_api"  + str(clusternum) + '.csv'
        alist.append([after_filter_cluster_filename, after_filter_pub_inf_filename, after_filter_pub_api_filename, after_filter_pri_inf_filename, after_filter_pri_api_filename])
    with open(filename, "w", newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)
    return alist


#generate public interface and api
def generatePublicApi_batch(filter, project, alg, filelist):
    apidetailFile = "../testcase_data/" + project + '/workflow/' +  project + '_workflow_publicAPIdetail.csv'
    for each in filelist:
        clusterFile = each[0]
        pubinterfaceFile = each[1]
        pubapiFile = each[2]
        cmd = 'python ../measure/identifyPublicInterface.py ' +  apidetailFile + ' ' + clusterFile + ' ' + pubinterfaceFile + ' ' + pubapiFile
        returncode  = subprocess.call(cmd, shell=True)


#step2: generate api file for the filtered clsuters.
#step3: measure api num, inter-call, and such metrics.
def generatePrivateApi_batch(filter, project,method,filename):
    print("api measure start......")
    workflow_filename = '../testcase_data/' + project + '/workflow/' + project + '_workflow_reduced.csv'

    clusterAPICmd = 'python  analyzeClusterAndAPI.py  ' +  workflow_filename + ' '  + filename
    returncode  = subprocess.call(clusterAPICmd, shell=True)



def measurePublicCohesion_batch(project, method, filelist):
    #metric == 'private-dom':
    print("public dom cohesion measure start......")
    cmd1 = 'python ../measure/tosc-interf-dom-cohesion.py  '
    for each in filelist:
        after_filter_cluster_api_filename = each[2]
        this_cmd = cmd1 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)

    #metric == 'private-msg':
    print("public msg cohesion measure start......")
    cmd2 = 'python ../measure/tosc-interf-msg-cohesion.py '
    for each in filelist:
        after_filter_cluster_api_filename = each[2]
        this_cmd = cmd2 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)


#step4: measure CHM and CHD metrics.
def measurePrivateCohesion_batch(filter, project, method, filelist):
    #metric == 'private-dom':
    print("dom-cohesion measure start......")
    cmd1 = 'python ../measure/tosc-interf-dom-cohesion.py  '
    for each in filelist:
        after_filter_cluster_api_filename = each[4]
        this_cmd = cmd1 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)

    #metric == 'private-msg':
    print("msg-cohesion measure start......")
    cmd2 = 'python ../measure/tosc-interf-msg-cohesion.py '
    for each in filelist:
        after_filter_cluster_api_filename = each[4]
        this_cmd = cmd2 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)


def measure_ioe_batch(project, method, filename, ioe_old_file, ioe_new_file):
    print("ioe measure start...")
    commitfile ='../testcase_data/' + project + '/dependency/' + project + "cmt.csv"
    cmd = "python ../measure/ioe-measure.py " + commitfile + " " + method + " " + filename + " " + ioe_old_file + " " + ioe_new_file
    returncode  = subprocess.call(cmd, shell=True)

def measure_modularity_batch(project, filter, fileListFile, modularity_file):
    classfileName_withcoverage = '../testcase_data/improvement/fv/' + project + '_testcase_class_' + filter + '.csv'
    calldepfileName_withccoverage = '../testcase_data/improvement/calldep/' + project + '_calldep_' + filter + '.csv'
    concerndepFileName = '../testcase_data/improvement/concerndep/' + project + '_concerndep.csv'
    cmd_list = ['python']
    cmd_list.append('../measure/modularity/modularity-measure.py')
    cmd_list.append(classfileName_withcoverage)
    cmd_list.append(calldepfileName_withccoverage)
    cmd_list.append(concerndepFileName)
    cmd_list.append(fileListFile)
    cmd_list.append(modularity_file) #outfile containing measures
    cmd = '  '.join(cmd_list)
    returncode  = subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    project = sys.argv[1]
    alg = sys.argv[2] # #wca-uem, limb
    filter = sys.argv[3] #all
    #interface = sys.argv[3] #private
    #metric = sys.argv[4] #private-dom, private-msg
    servnum_start = int(sys.argv[4])
    servnum_end = int(sys.argv[5])
    ioe_old_file = sys.argv[6]#detail value for each service
    ioe_new_file = sys.argv[7]#final value fot the system

    modularity_file = sys.argv[8] #modularity measures

    #step1: filter the clusters by using tescase class benchmark
    #filter_batch(filter, project, servnum_start,servnum_end,alg)
    #print("finish filter batch")


    filename= "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + alg + "-filter-" + filter + "/" + project + "_beprocessedList.csv"
    filelist = genFilelistFile(filter, project,servnum_start, servnum_end, alg, filename)


    #generate public interface and api
    #generatePublicApi_batch(filter, project, alg, filelist)
    measurePublicCohesion_batch(project, alg, filelist)
    '''
    #step2:generate api file for the filtered clsuters.
    #step3: measure api num, inter-call, and such metrics. into log
    generatePrivateApi_batch(filter, project, alg, filename)
    #step4: measure CHM and CHD metrics.
    measurePrivateCohesion_batch(filter, project, alg, filelist)
    #print("finish cohesion measurement batch")
    '''
    #step5:measure ioe
    #measure_ioe_batch(project, alg, filename, ioe_old_file, ioe_new_file)
    #print("finish ioe measuremnt batch")

    #measure modularity
    #measure_modularity_batch(project, filter, filename, modularity_file)
