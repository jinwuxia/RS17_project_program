import os
import subprocess
if __name__ == '__main__':

    '''
    #jforum219
    cluster_file_name = 'data/jforum219/jforum219_'
    workflow_file_name = 'data/jforum219/jforum219_workflow_reduced.csv'
    api_file_name = 'data/jforum219/jforum219_'
    '''


    #jpetstore6
    cluster_file_name = 'data/jpetstore6/jpetstore6_'
    workflow_file_name = 'data/jpetstore6/jpetstore6_workflow_reduced.csv'
    api_file_name = 'data/jpetstore6/jpetstore6_'


    #for servnum in range(16,48):
    for servnum in range(1,24):
        this_cluster_file_name = cluster_file_name + str(servnum) + '_cluster.csv'
        this_api_file_name =  api_file_name + str(servnum) + '_clusterAPI.csv'
        cmd = 'python  analyzeClusterAndAPI.py  ' +  this_cluster_file_name + '  ' +   workflow_file_name + '  '  +  this_api_file_name
        returncode  = subprocess.call(cmd)
        #print returncode
