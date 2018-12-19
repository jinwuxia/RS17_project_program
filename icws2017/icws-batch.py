import os
import subprocess
import sys
import csv

'''
usage:
python icws-batch.py
[project=]xwiki-plarform108
[method=]icws
[filter=]all
[pkgpre=]org.xwiki
[ioe-old_file=]ioe-measure_old.file
[ioe-new-file=]ioe-measure_new.file
> workflow-iof-measure.log

the prepared file include:
data/project/
data/project/$project$-icws-filter-$filter$/
project.udb
project_all_class.txt
../testcase-data/project/workflow/project_workflow_reduce.csv
filterclassfile= $project$_testcase_$filter$_class.csv
'''
#uperl identifierParser.pl  jpetstore6.udb  org.mybatis.jpetstore   jpetstore6_words.txt
def generate_all_feature(project, projectPkgName):
    datadir = "data/" + project + "/"
    udbfile = datadir + project + ".udb"
    wordfile = datadir + project + "_words.txt"
    parseWords_cmd = "uperl identifierParser.pl  " + udbfile +  " " + projectPkgName + " " +  wordfile
    print(parseWords_cmd)
    returncode  = subprocess.call(parseWords_cmd, shell=True)
    print("finish word parser........")

    synfile = datadir + project + "syn.csv"
    semantic_cmd = "python semanticParser.py " + wordfile + " " + synfile
    print(semantic_cmd)
    returncode  = subprocess.call(semantic_cmd, shell=True)
    print("finish semantic parser......")

    simfile = datadir + project + "synsim.csv"
    cosion_cmd = "python semanticCosin.py " + synfile + " " + simfile
    print(cosion_cmd)
    returncode  = subprocess.call(cosion_cmd, shell=True)
    print("finish sim matrix......")

    #count the coverage when use different   sim threshold
    static_all_class_file = datadir + "_all_class.txt"
    statiscmd = "python classstatis.py" +  static_all_class_file + " " + simfile
    print(statiscmd)
    returncode  = subprocess.call(statiscmd, shell=True)
    print("finish coverage statis.......")




#step1: clustering
def cluster_filter_batch(filter, project,servnum_start, servnum_end, method):
    #use class benchmark to filter the sim file
    datadir = "data/" + project + "/"
    simfile = datadir + project + "synsim.csv"
    filterClassFile = datadir + project + "_testcase_" + filter + "_class.csv"
    after_filter_simfile = datadir + project + "synsim_filter_" + filter + ".csv"
    cmd = "python semanticFilter.py " +  filterClassFile + " " + simfile + " " + after_filter_simfile
    print(cmd)
    returncode  = subprocess.call(cmd, shell=True)
    print("finish synsim filter.....")

    for servnum in range(servnum_start, servnum_end):
        filterdir = datadir + project + "-" + method + "-filter-" + filter + "/"
        cluterfileName = filterdir + project + "_" + str(servnum)+ '_cluster.csv'
        cmd = ('python mstClustering.py ' +  after_filter_simfile + '  '  + cluterfileName + '  ' +  str(servnum) )
        print (cmd)
        returncode  = subprocess.call(cmd, shell=True)
    print("finish clutering.....")


def genFilelistFile(filter, project,servnum_start, servnum_end, method, filename):
    alist=list()
    for clusternum in range(servnum_start, servnum_end + 1):
        after_filter_cluster_filename = "data/" + project + "/" + project + "-" + method + "-filter-" + filter + "/" + project + "_" + str(clusternum) + "_cluster.csv"
        after_filter_pub_inf_filename = "data/" + project + "/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_" + str(clusternum) + '_pub_inf.csv'
        after_filter_pub_api_filename = "data/" + project + "/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_" + str(clusternum) + '_pub_api.csv'
        after_filter_pri_inf_filename = "data/" + project + "/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_" + str(clusternum) + '_pri_inf.csv'
        after_filter_pri_api_filename = "data/" + project + "/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_" + str(clusternum) + '_pri_api.csv'
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



#step4: measure CHM and CHD metrics.
def measurePublicCohesion_batch(filter, project, method, filelist):
    #metric == 'private-dom':
    print("dom-cohesion measure start......")
    cmd1 = 'python ../measure/tosc-interf-dom-cohesion.py  '
    for each in filelist:
        after_filter_cluster_api_filename = each[2]
        #after_filter_cluster_api_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_clusterAPI"  + str(clusternum) + '.csv'
        this_cmd = cmd1 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)

    #metric == 'private-msg':
    print("msg-cohesion measure start......")
    cmd2 = 'python ../measure/tosc-interf-msg-cohesion.py '
    for each in filelist:
        after_filter_cluster_api_filename = each[2]
        #after_filter_cluster_api_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_clusterAPI"  + str(clusternum) + '.csv'
        this_cmd = cmd2 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)


#step4: measure CHM and CHD metrics.
def measurePrivateCohesion_batch(filter, project, method, filelist):
    #metric == 'private-dom':
    print("dom-cohesion measure start......")
    cmd1 = 'python ../measure/tosc-interf-dom-cohesion.py  '
    for each in filelist:
        after_filter_cluster_api_filename = each[4]
        #after_filter_cluster_api_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_clusterAPI"  + str(clusternum) + '.csv'
        this_cmd = cmd1 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)

    #metric == 'private-msg':
    print("msg-cohesion measure start......")
    cmd2 = 'python ../measure/tosc-interf-msg-cohesion.py '
    for each in filelist:
        after_filter_cluster_api_filename = each[4]
        #after_filter_cluster_api_filename = "../testcase_data/" + project + "/traditional_clustering/"  + project + "-" + method + "-filter-" + filter + "/" + project + "_clusterAPI"  + str(clusternum) + '.csv'
        this_cmd = cmd2 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)


def measure_ioe_batch(project, method, filelistfilename, ioe_old_file, ioe_new_file):
    print("ioe measure start...")
    commitfile ='../testcase_data/' + project + '/dependency/' + project + "cmt.csv"
    cmd = "python ../measure/ioe-measure.py " + commitfile + " " + method + " " + filelistfilename + " " + ioe_old_file + " " + ioe_new_file
    returncode  = subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    project = sys.argv[1]
    alg = sys.argv[2] #icws
    filter = sys.argv[3] #all
    projectPkgName = sys.argv[4] #org.xwiki
    #interface = sys.argv[3] #private
    #metric = sys.argv[4] #private-dom, private-msg
    servnum_start = int(sys.argv[5])
    servnum_end = int(sys.argv[6])
    ioe_old_file = sys.argv[7] #detail value for each service
    ioe_new_file = sys.argv[8] #final value fot the system

    '''
    if project == 'jforum219':
        servnum_start = 16
        servnum_end = 47
    elif project == 'jpetstore6':
        servnum_start = 1
        servnum_end = 23
    elif project == 'roller520':
        servnum_start = 2
        servnum_end = 72
    elif project == 'xwiki-platform108':
        servnum_start = 2
        servnum_end = 199
    '''


    #step1: generate feature simfile.
    #generate_all_feature(project, projectPkgName)

    #step2: clustering
    #cluster_filter_batch (filter, project,servnum_start, servnum_end, alg)



    filename= "data/" + project + "/" + project + "-" + alg + "-filter-" + filter + "/" + project + "_beprocessedList.csv"
    filelist = genFilelistFile(filter, project,servnum_start, servnum_end, alg, filename)


    #generate public interface and api
    #step: measure CHM and CHD metrics.
    generatePublicApi_batch(filter, project, alg, filelist)
    measurePublicCohesion_batch(filter, project, alg, filelist)

    #step2:generate api file for the filtered clsuters.
    #step3: measure api num, inter-call, and such metrics. into log
    generatePrivateApi_batch(filter, project, alg, filename)
    measurePrivateCohesion_batch(filter, project, alg, filelist)


    #6:measure ioe
    #measure_ioe_batch(project, alg, filename, ioe_old_file, ioe_new_file)
    #print("finish ioe measuremnt batch")
