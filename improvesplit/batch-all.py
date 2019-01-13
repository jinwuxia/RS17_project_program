import sys
import csv
import os
import subprocess

'''
collectPublicAPI.py shoud be runned before.

'''
#[clusterfile, public_interfacefile, public_api_file, privateInterfacefile, privateapifile]
def getFileList(folder):
    listlist = list()
    #folder = "/home/ubuntu/Desktop/temp/poem"
    for file in os.listdir(folder):
        #print (file)
        filepath = os.path.join(folder, file)
        #print (filepath)
        pre = filepath.split(".csv")[0]
        publicInterfaceFile = pre + "_pub_inf.csv"
        publicApiFile = pre + "_pub_api.csv"
        privateInterfaceFile = pre + "_pri_inf.csv"
        privateApiFile = pre + "_pri_api.csv"
        listlist.append([filepath, publicInterfaceFile, publicApiFile, privateInterfaceFile, privateApiFile])
    return listlist


#getFileList(sys.argv[1])


def writecsv(alist, filename):
    with open(filename, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)



#generate public interface and api
def generatePublicApi_batch(project, filelist):
    apidetailFile = "../testcase_data/" + project + '/workflow/' +  project + '_workflow_publicAPIdetail.csv'
    for each in filelist:
        clusterFile = each[0]
        pubinterfaceFile = each[1]
        pubapiFile = each[2]
        cmd = 'python ../measure/identifyPublicInterface.py ' +  apidetailFile + ' ' + clusterFile + ' ' + pubinterfaceFile + ' ' + pubapiFile
        returncode  = subprocess.call(cmd, shell=True)

#step2: generate api file for the filtered clsuters.
#step3: measure api num, inter-call, and such metrics.
def generatePrivateApi_batch(project, filename):
    print("api measure start......")
    workflow_filename = '../testcase_data/' + project + '/workflow/' + project + '_workflow_reduced.csv'

    clusterAPICmd = 'python  analyzeClusterAndAPI.py  ' +  workflow_filename + ' '  + filename
    returncode  = subprocess.call(clusterAPICmd, shell=True)


def measurePublicCohesion_batch(project, method, filelist):
    #metric == 'private-dom':
    #print("public dom cohesion measure start......")
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
def measurePrivateCohesion_batch(project, method, filelist):
    #metric == 'private-dom':
    print("private dom cohesion measure start......")
    cmd1 = 'python ../measure/tosc-interf-dom-cohesion.py  '
    for each in filelist:
        after_filter_cluster_api_filename = each[4]
        this_cmd = cmd1 + after_filter_cluster_api_filename + " " + method
        returncode  = subprocess.call(this_cmd, shell=True)

    #metric == 'private-msg':
    print("private msg cohesion measure start......")
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
    alg = sys.argv[2] # fom
    filter = sys.argv[3] #all, 20percent, 40percent, 60percent, 80percent
    ioe_old_file = sys.argv[4]#detail value for each service
    ioe_new_file = sys.argv[5]#final value fot the system
    fileFolder = sys.argv[6] #clusterfiles folder
    modularity_file = sys.argv[7] #modularity file

    filelist = getFileList(fileFolder)
    filelistfile = "../testcase_data/"  + project + "/coreprocess/" + project + "_beprocessedList.csv"
    writecsv(filelist, filelistfile)


    #step1:generate public interface and api file for the clusters.
    generatePublicApi_batch(project, filelist)
    #2: measure CHM and CHD metrics for public
    measurePublicCohesion_batch(project, alg, filelist)
    #print("finish public cohesion measurement batch")

    #step2:generate private api file for the  clusters.
    #step3: measure private api num, inter-call, and such metrics. into log
    #generatePrivateApi_batch(project, filelistfile)
    #step4: measure CHM and CHD metrics.
    #measurePrivateCohesion_batch(project, alg, filelist)
    #print("finish private cohesion measurement batch")

    #step6:measure ioe
    #measure_ioe_batch(project, alg, filelistfile, ioe_old_file, ioe_new_file)
    #print("finish ioe measuremnt batch")


    #step 7: measure dynamic cohesion , coupling and semantic cohesion, acoupling.
    measure_modularity_batch(project, filter, filelistfile, modularity_file)
