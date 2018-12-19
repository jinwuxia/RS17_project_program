import sys
import os
import subprocess

#notice: we should use the  simsyn.csv file after filter.
'''
for servnum in range(16,48):
    inputfileName = 'data/jforum219/jforum219synsim.csv'
    outfileName = 'data/jforum219/jforum219_' + str(servnum)+ '_cluster.csv'
    cmd = ('python mstClustering.py ' +  inputfileName + '  '  + outfileName + '  ' +  str(servnum) )
    returncode  = subprocess.call(cmd)

'''
'''
for servnum in range(2,73):
    inputfileName = 'data/roller520/roller520synsim.csv'
    outfileName = 'data/roller520/clusters/roller520_' + str(servnum)+ '_cluster.csv'
    cmd = ('python mstClustering.py ' +  inputfileName + '  '  + outfileName + '  ' +  str(servnum) )
    print cmd

    returncode  = subprocess.call(cmd, shell=True)
'''

for servnum in range(2,200):
    #use 100% testcase class to filter
    inputfileName = 'data/xwiki-platform108/xwiki-platform108synsim_filter_ts_all.csv'

    outfileName = 'data/xwiki-platform108/clusters-TS-all-as-benchmark/xwiki-platform108_' + str(servnum)+ '_cluster.csv'
    cmd = ('python mstClustering.py ' +  inputfileName + '  '  + outfileName + '  ' +  str(servnum) )
    print (cmd)

    returncode  = subprocess.call(cmd, shell=True)
