import os
import subprocess
if __name__ == '__main__':

    '''
    #jforum219   limbo
    cluster_file_name = '../testcase_data/jforum219_1/traditional_clustering/jforum219-limbo/jwx_limbo_ilm_LIMBO_preselected_ilm_'
    workflow_file_name = '../testcase_data/jforum219_1/workflow/jforum219_workflow_reduced.csv'
    api_file_name = '../testcase_data/jforum219_1/traditional_clustering/jforum219-limbo/limbo_'
    '''
    '''
    #jforum219   wca uem
    cluster_file_name = '../testcase_data/jforum219_1/traditional_clustering/jforum219-wca-uem/jwx_wca_uem_WCA_preselected_uem_'
    workflow_file_name = '../testcase_data/jforum219_1/workflow/jforum219_workflow_reduced.csv'
    api_file_name = '../testcase_data/jforum219_1/traditional_clustering/jforum219-wca-uem/wca_'
    '''
    '''
    #jpetstore6   limbo
    cluster_file_name = '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-limbo/jwx_limbo_ilm_LIMBO_preselected_ilm_'
    workflow_file_name = '../testcase_data/jpetstore6/workflow/jpetstore6_workflow_reduced.csv'
    api_file_name = '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-limbo/limbo_'
    '''


    #jpetstore6 wca
    cluster_file_name = '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-wca-uem/jwx_wca_uem_WCA_preselected_uem_'
    workflow_file_name = '../testcase_data/jpetstore6/workflow/jpetstore6_workflow_reduced.csv'
    api_file_name = '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-wca-uem/wca_'

    #for servnum in range(16,48):
    for servnum in range(1,24):
        this_cluster_file_name = cluster_file_name + str(servnum) + '_clusters.rsf.csv'
        this_api_file_name = api_file_name + str(servnum) + '_clusterAPI.csv'
        cmd = 'python  analyzeClusterAndAPI.py  ' +  this_cluster_file_name + '  ' +   workflow_file_name + '  '  +  this_api_file_name
        returncode  = subprocess.call(cmd)
        #print returncode
