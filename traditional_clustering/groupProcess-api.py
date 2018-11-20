import os
import subprocess
import sys

if __name__ == '__main__':

    from os import walk
    fileList=[]
    for (dirpath, dirnames, filenames) in walk('../testcase_data/repeat3group'):
        for name in filenames:
            if 'cluster' in name and 'clusterAPI' not in name:
                f = dirpath + '/' + name
                fileList.append(f)
                print (f, '\n\n')

    for clusterFileName in fileList :
        #print clusterFileName
        preList = clusterFileName.split('/')
        simpleClusterFileName = preList[-1]
        project = simpleClusterFileName.split('_')[0]
        servnum = simpleClusterFileName.split('_')[1]
        if project == 'jpetstore6':
            workflowFileName = '../testcase_data/' + project + '/workflow/' + project + '_workflow_reduced.csv'
        if project == 'roller520':
            workflowFileName = '../testcase_data/' + project + '/workflow/' + project + '_workflow_reduced.csv'
        if project == 'bvn13':
            workflowFileName = '../testcase_data/' + project + '/workflow/' + project + '_workflow_reduced.csv'
        if project == 'solo270':
            workflowFileName = '../testcase_data/' + project + '/workflow/' + project + '_workflow_reduced.csv'
        if project == 'jforum219':
            workflowFileName = '../testcase_data/' + 'jforum219_1' + '/workflow/' + project + '_workflow_reduced.csv'

        apiFileName = project + '_' + servnum + '_clusterAPI.csv'
        print (clusterFileName, apiFileName)

        cmd = 'python  ../split/coreprocess/getComponentProAPI.py  ' +  clusterFileName + '  ' +   workflowFileName + '  '  +  apiFileName
        #cmd = 'python  analyzeClusterAndAPI.py  ' +  clusterFileName + '  ' +   workflowFileName + '  '  +  apiFileName
        #print cmd
        returncode  = subprocess.call(cmd, shell=True)
        #print returncode
