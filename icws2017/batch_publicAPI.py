import os
import sys
import subprocess


#python pro.py  project
if __name__ == '__main__':
    project = sys.argv[1]

    if project == 'jforum219':
        testcase_name =     'data/jforum219/jforum219_testcase_name.csv'
        cluster_file_name = 'data/jforum219/jforum219_'
        api_file_name =     'data/jforum219/jforum219_public_'
        servnum_start = 16
        servnum_end = 47
        PRE = 'net.jforum.view.forum'

    if project == 'jpetstore6':
        testcase_name =     'data/jpetstore6/jpetstore6_testcase_name.csv'
        cluster_file_name = 'data/jpetstore6/jpetstore6_'
        api_file_name =     'data/jpetstore6/jpetstore6_public_'
        servnum_start = 1
        servnum_end = 23
        PRE = 'org.mybatis.jpetstore.web.actions'

    for servnum in range(servnum_start, servnum_end + 1):
        this_cluster_file_name = cluster_file_name + str(servnum) + '_cluster.csv'
        this_api_file_name = api_file_name + str(servnum) + '_clusterAPI.csv'
        cmd = 'python publicAPI.py  ' + testcase_name  + '  ' +  this_cluster_file_name  + ' ' +  this_api_file_name   + '  ' + PRE
        returncode  = subprocess.call(cmd)
