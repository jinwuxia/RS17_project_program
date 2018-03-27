import sys
import os
import subprocess

''' batch_getcomponentAPI.sh extract all clusters api
But this file is for extracting api of the specified clusters
for given_m best ans,
extract api for serv_thr clusterfile
python pro.py project
'''

project = sys.argv[1]

if project == 'solo270':
    servnum_thr_pair_list = [[8,0.2],  [6,0.4],   [7,0.3],   [7,0.4],   [7,0.5]]
    thr_cluster_file = '../../../testcase_data/solo270/coreprocess/optionA-enum/solo270_testcase1_clusters_'
    serv_cluster_file = '../../../testcase_data/solo270/coreprocess/testcaseClustering/solo270_testcase1_jm_AVG_'
    workflow_file = '../../../testcase_data/solo270/workflow/solo270_workflow_reduced.csv'
    api_file = '../../../testcase_data/solo270/coreprocess/optionA-enum/solo270_testcase1_'


elif project == 'bvn13': #for
    servnum_thr_pair_list = [[4,0.2],  [5,1.0],   [5,0.3],   [7,0.3],   [6,0.3]]
    thr_cluster_file = '../../../testcase_data/bvn13/coreprocess/optionA-enum/bvn13_testcase1_clusters_'
    serv_cluster_file = '../../../testcase_data/bvn13/coreprocess/testcaseClustering/bvn13_testcase1_jm_AVG_'
    workflow_file = '../../../testcase_data/bvn13/workflow/bvn13_workflow_reduced0.csv'
    api_file = '../../../testcase_data/bvn13/coreprocess/optionA-enum/bvn13_testcase1_'


elif project == 'jforum219': #for jpetstore219
    servnum_thr_pair_list = [[16,0.01],[17,0.01],[18,0.01],[19,0.01],[20,0.01],[21,0.01],\
    [22,0.01],[22,0.02],[22,0.03],[23,0.01],[23,0.05],[23,0.06],[23,1.00],[24,0.06],[25,0.08],\
    [26,0.08],[26,0.06],[26,0.10],[27,0.08],[27,0.10],[28,0.02],[29,0.02],[30,0.02],[31,0.02],[32,0.01],[32,0.02],[33,0.02],\
    [33,0.06],[33,0.11],[33,0.14],[34,0.02],[34,0.03],[35,0.02],[35,0.03],[36,0.01],[36,0.02],[36,0.03],[37,0.03],[38,0.03],\
    [39,0.02],[40,0.02],[41,0.02],[42,0.02],[43,0.02],[44,0.02],[45,0.03],[45,0.08],[46,0.03],[46,0.08],[46,0.15],[46,0.18],\
    [46,0.27],[46,0.25],[46,0.26],[46,0.44],[46,1.00],[47,0.03],[47,0.08],[47,0.15],[47,0.18],[47,0.25],[47,0.26],[47,0.27],\
    [47,0.44],[47,1.00]]
    thr_cluster_file = '../../../testcase_data/jforum219_1/coreprocess/optionA-enum/jforum219_testcase1_clusters_'
    serv_cluster_file = '../../../testcase_data/jforum219_1/coreprocess/testcaseClustering/jforum219_testcase1_jm_AVG_'
    workflow_file = '../../../testcase_data/jforum219_1/workflow/jforum219_workflow_reduced.csv'
    api_file = '../../../testcase_data/jforum219_1/coreprocess/optionA-enum/jforum219_testcase1_'


elif project == 'jpetstore6': #for jpetstore6
    servnum_thr_pair_list = [[1,0.01],[2,0.06],[3,0.23],[3,0.26],[4,0.18],\
        [4,0.21],[5,0.08],[6,0.18],[7,0.14],[7,0.25], [8,0.14], [8,0.25], [9,0.34],[10,0.24]]
    thr_cluster_file = '../../../testcase_data/jpetstore6/coreprocess/optionA-enum/jpetstore6_testcase1_clusters_'
    serv_cluster_file = '../../../testcase_data/jpetstore6/coreprocess/testcaseClustering/jpetstore6_testcase1_jm_AVG_'
    workflow_file = '../../../testcase_data/jpetstore6/workflow/jpetstore6_workflow_reduced.csv'
    api_file = '../../../testcase_data/jpetstore6/coreprocess/optionA-enum/jpetstore6_testcase1_'

for [servnum, thr_int] in servnum_thr_pair_list:
    this_thr_cluster_file = (thr_cluster_file + str(servnum)   + '_' + str(thr_int) +'.csv')
    this_serv_cluster_file = (serv_cluster_file + str(servnum) + '.csv')
    this_api_file = (api_file + str(servnum) + '_' + str(thr_int) + '_clustersAPI.csv')
    cmd = 'python ../getComponentAPI.py ' +  this_thr_cluster_file + ' ' \
        +  this_serv_cluster_file  + ' ' + workflow_file + ' ' +  this_api_file
    print cmd
    #returncode  = subprocess.call(cmd)
    os.system(cmd)
