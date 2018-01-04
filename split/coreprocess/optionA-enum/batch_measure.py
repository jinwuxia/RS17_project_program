import sys
import os
import subprocess
import csv

'''
for given_m best ans and its clusterAPI file,
measure interface quality for clusterAPI file,
python pro.py project interface
'''

project = sys.argv[1]
metric  = sys.argv[2]
interface = sys.argv[3]

if metric == 'private-dom-cohesion':
    cmd = 'python ../../../measure/tosc-interf-dom-cohesion.py '
elif metric == 'private-msg-cohesion':
    cmd = 'python ../../../measure/tosc-interf-msg-cohesion.py '



if project == 'jforum219': #for jforum219
    fileName = '../../../testcase_data/jforum219_1/coreprocess/optionB-search/jforum219_pareto_analysis_servnum_best_norepeat.csv'
    servnum_thr_pair_list = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            if each[0] == 'servnum':
                continue
            servnum = int(each[0])
            thr = round(int(each[1]) / float(100), 2)
            servnum_thr_pair_list.append([servnum, thr])
    if interface == 'private':
        api_file = '../../../testcase_data/jforum219_1/coreprocess/optionA-enum/jforum219_testcase1_'


elif project == 'jpetstore6': #for jpetstore6
    fileName = '../../../testcase_data/jpetstore6/coreprocess/optionB-search/jpetstore6_pareto_analysis_servnum_best_norepeat.csv'
    servnum_thr_pair_list = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            if each[0] == 'servnum':
                continue
            servnum = int(each[0])
            thr = round(int(each[1]) / float(100), 2)
            servnum_thr_pair_list.append([servnum, thr])
    if interface == 'private':
        api_file = '../../../testcase_data/jpetstore6/coreprocess/optionA-enum/jpetstore6_testcase1_'

elif project == 'roller520': # for roller520
    fileName = '../../../testcase_data/roller520/coreprocess/optionB-search/roller520_pareto_analysis_servnum_best_norepeat.csv'
    servnum_thr_pair_list = list()
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            if each[0] == 'servnum':
                continue
            servnum = int(each[0])
            thr = round(int(each[1]) / float(100), 2)
            servnum_thr_pair_list.append([servnum, thr])
    if interface == 'private':
        api_file = '../../../testcase_data/roller520/coreprocess/optionA-enum/roller520_testcase1_'

for [servnum, thr_int] in servnum_thr_pair_list:
    thr_int = ('%.2f' % thr_int)
    #print thr_int
    if interface == 'private':
        this_api_file = (api_file + str(servnum) + '_' + str(thr_int) + '_clustersAPI.csv')
    elif interface == 'public':
        this_api_file = (api_file + str(servnum) + '.csv')

    this_cmd =  cmd + this_api_file
    #print this_cmd
    #returncode  = subprocess.call(cmd)
    os.system(this_cmd)
