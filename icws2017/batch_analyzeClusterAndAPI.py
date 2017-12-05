import os
import subprocess

#python pro.py  project
if __name__ == '__main__':
    project = sys.argv[1]

    if project == 'jforum219':
        #jforum219
        cluster_file_name = 'data/jforum219/jforum219_'
        workflow_file_name = 'data/jforum219/jforum219_workflow_reduced.csv'
        api_file_name = 'data/jforum219/jforum219_'
        start = 16
        end = 48

    if project == 'jpetstore6':
        #jpetstore6
        cluster_file_name = 'data/jpetstore6/jpetstore6_'
        workflow_file_name = 'data/jpetstore6/jpetstore6_workflow_reduced.csv'
        api_file_name = 'data/jpetstore6/jpetstore6_'
        start = 1
        end = 24

    for servnum in range(start,end):
        this_cluster_file_name = cluster_file_name + str(servnum) + '_cluster.csv'
        this_api_file_name =  api_file_name + str(servnum) + '_clusterAPI.csv'
        cmd = 'python  analyzeClusterAndAPI.py  ' +  this_cluster_file_name + '  ' +   workflow_file_name + '  '  +  this_api_file_name
        returncode  = subprocess.call(cmd)
        #print returncode
