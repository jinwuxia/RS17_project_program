import os
import sys
import subprocess


#python pro.py  roject alg
if __name__ == '__main__':
    project = sys.argv[1]
    alg = sys.argv[2]
    if project == 'jforum219' and alg == 'wca':
        testcase_name = ' ../testcase_data/jforum219_1/workflow/jforum219_testcase_name.csv'
        cluster_file_name = '../testcase_data/jforum219_1/traditional_clustering/jforum219-wca-uem/jwx_wca_uem_WCA_preselected_uem_'
        api_file_name =     '../testcase_data/jforum219_1/traditional_clustering/jforum219-wca-uem/public_wca_uem_'
        servnum_start = 16
        servnum_end = 47
        PRE = 'net.jforum.view.forum'

    elif project == 'jforum219' and alg == 'limbo':
        testcase_name = ' ../testcase_data/jforum219_1/workflow/jforum219_testcase_name.csv'
        cluster_file_name = '../testcase_data/jforum219_1/traditional_clustering/jforum219-limbo/jwx_limbo_ilm_LIMBO_preselected_ilm_'
        api_file_name =     '../testcase_data/jforum219_1/traditional_clustering/jforum219-limbo/public_limbo_uem_'
        servnum_start = 16
        servnum_end = 47
        PRE = 'net.jforum.view.forum'

    elif project == 'jpetstore6' and alg == 'wca':
        testcase_name = ' ../testcase_data/jpetstore6/workflow/jpetstore6_testcase_name.csv'
        cluster_file_name = '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-wca-uem/jwx_wca_uem_WCA_preselected_uem_'
        api_file_name =     '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-wca-uem/public_wca_uem_'
        servnum_start = 1
        servnum_end = 23
        PRE = 'org.mybatis.jpetstore.web.actions'

    elif project == 'jpetstore6' and alg == 'limbo':
        testcase_name = ' ../testcase_data/jpetstore6/workflow/jpetstore6_testcase_name.csv'
        cluster_file_name = '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-limbo/jwx_limbo_ilm_LIMBO_preselected_ilm_'
        api_file_name =     '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-limbo/public_limbo_uem_'
        servnum_start = 1
        servnum_end = 23
        PRE = 'org.mybatis.jpetstore.web.actions'

    for servnum in range(servnum_start, servnum_end + 1):
        this_cluster_file_name = cluster_file_name + str(servnum) + '_clusters.rsf.csv'
        this_api_file_name = api_file_name + str(servnum) + '_clusterAPI.csv'
        cmd = 'python publicAPI.py  ' + testcase_name  + '  ' +  this_cluster_file_name  + ' ' +  this_api_file_name + ' ' + PRE
        returncode  = subprocess.call(cmd)
