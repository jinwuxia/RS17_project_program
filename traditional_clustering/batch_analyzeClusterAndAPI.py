import os
import subprocess
import sys

if __name__ == '__main__':
    project = sys.argv[1]  #jpetstore6, jforum219, roller520
    alg = sys.argv[2]      #wca, limbo
    cluster_start = int(sys.argv[3])   #cluster_num_min
    cluster_end = int(sys.argv[4])   #cluster_num_max

    workflow_file_name = '../testcase_data/' + project + '/workflow/' + project + '_workflow_reduced.csv'
    if alg == 'wca':
        cluster_file_name = ('../testcase_data/' + project + '/traditional_clustering/wca/clusters/jwx_wca_uem_WCA_preselected_uem_')
        api_file_name     = ('../testcase_data/' + project + '/traditional_clustering/wca/clusterAPI/' + project + '_wca_')
    elif alg == 'limbo':
        cluster_file_name = ('../testcase_data/' + project + '/traditional_clustering/limbo/clusters/jwx_limbo_ilm_LIMBO_preselected_ilm_')
        api_file_name     = ('../testcase_data/' + project + '/traditional_clustering/limbo/clusterAPI/' + project + '_limbo_')
    else:
        print 'unknown ' + alg

    for servnum in range(cluster_start, cluster_end + 1):
        this_cluster_file_name = cluster_file_name + str(servnum) + '_clusters.rsf.csv'
        this_api_file_name = api_file_name + str(servnum) + '_clusterAPI.csv'
        cmd = 'python  analyzeClusterAndAPI.py  ' +  this_cluster_file_name + '  ' +   workflow_file_name + '  '  +  this_api_file_name
        #print cmd
        returncode  = subprocess.call(cmd, shell=True)
        #print returncode
