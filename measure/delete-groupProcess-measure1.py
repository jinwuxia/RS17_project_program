import os
import subprocess
import sys



if __name__ == '__main__':
    method = sys.argv[1] #icws
    fileType = sys.argv[2] #fome or others
    dir = sys.argv[3] #'../testcase_data/3group/icws'
    from os import walk
    fileList=[]
    for (dirpath, dirnames, filenames) in walk(dir):
        for name in filenames:
            if ('cluster' in name) and ('clusterAPI' not in name):
                f = dirpath + '/' + name
                fileList.append(f)
                print f
    print '\n\n'

    for clusterFileName in fileList :
        print clusterFileName
        preList = clusterFileName.split('/')
        simpleClusterFileName = preList[-1]
        project = simpleClusterFileName.split('_')[0]
        servnum = simpleClusterFileName.split('_')[1]
        if project == 'jpetstore6':
            commitFileName = '../testcase_data/' + project + '/dependency/' + project + 'cmt.csv'
        if project == 'roller520':
            commitFileName = '../testcase_data/' + project + '/dependency/' + project + 'cmt_simple.csv'
        if project == 'bvn13':
            commitFileName = '../testcase_data/' + project + '/dependency/' + project + 'cmt.csv'
        if project == 'solo270':
            commitFileName = '../testcase_data/' + project + '/dependency/' + project + 'cmt.csv'
        if project == 'jforum219':
            commitFileName = '../testcase_data/' + 'jforum219_1' + '/dependency/' + project + 'cmt.csv'

        logFileName = 'm1_' + method + '_' + project  + '_' + servnum + '.csv'
        cmd = 'python  cochange_measure1_repeat.py  ' +  commitFileName + ' ' + clusterFileName + ' ' + fileType + ' > ' +  logFileName

        print cmd

        #cmd = 'python  measure/coreprocess/tosc-interf-dom-cohesion.py  ' +  apiFileName
        #cmd = 'python  measure/coreprocess/tosc-interf-msg-cohesion.py  ' +  apiFileName
        returncode  = subprocess.call(cmd, shell=True)
        #print returncode
