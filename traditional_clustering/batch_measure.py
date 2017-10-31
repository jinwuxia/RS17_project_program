import os
import sys
import subprocess


#python pro.py  project alg interface  metric
#METRIC = private-dom,  private-msg, public-dom
if __name__ == '__main__':
    project = sys.argv[1]
    alg = sys.argv[2]
    interface = sys.argv[3]
    metric = sys.argv[4]

    if project == 'jforum219':
        servnum_start = 16
        servnum_end = 47
    elif project == 'jpetstore6':
        servnum_start = 1
        servnum_end = 23


    if project == 'jforum219' and alg == 'wca':
        if interface == 'public':
            api_file_name =     '../testcase_data/jforum219_1/traditional_clustering/jforum219-wca-uem/public_wca_uem_'
        elif interface == 'private':
            api_file_name =     '../testcase_data/jforum219_1/traditional_clustering/jforum219-wca-uem/wca_'

    elif project == 'jforum219' and alg == 'limbo':
        if interface == 'public':
            api_file_name =     '../testcase_data/jforum219_1/traditional_clustering/jforum219-limbo/public_limbo_uem_'
        elif interface == 'private':
            api_file_name =     '../testcase_data/jforum219_1/traditional_clustering/jforum219-limbo/limbo_'

    elif project == 'jpetstore6' and alg == 'wca':
        if interface == 'public':
            api_file_name =     '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-wca-uem/public_wca_uem_'
        elif interface == 'private':
            api_file_name =     '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-wca-uem/wca_'

    elif project == 'jpetstore6' and alg == 'limbo':
        if interface == 'public':
            api_file_name =     '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-limbo/public_limbo_uem_'
        elif interface == 'private':
            api_file_name =     '../testcase_data/jpetstore6/traditional_clustering/jpetstore6-limbo/limbo_'

    if metric == 'private-dom':
        cmd = 'python ../measure/tosc-interf-dom-cohesion.py '
    elif metric == 'private-msg':
        cmd = 'python ../measure/tosc-interf-msg-cohesion.py '
    elif metric == 'public-dom':
        cmd = 'python ../measure/tosc-interf-dom-cohesion-public.py '

    for servnum in range(servnum_start, servnum_end + 1):
        this_api_file_name = (api_file_name + str(servnum) + '_clusterAPI.csv')
        this_cmd = (cmd + this_api_file_name)
        returncode  = subprocess.call(this_cmd)
