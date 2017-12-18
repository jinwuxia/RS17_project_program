import sys
import os
import subprocess
'''
for servnum in range(16,48):
    inputfileName = 'data/jforum219/jforum219synsim.csv'
    outfileName = 'data/jforum219/jforum219_' + str(servnum)+ '_cluster.csv'
    cmd = ('python mstClustering.py ' +  inputfileName + '  '  + outfileName + '  ' +  str(servnum) )
    returncode  = subprocess.call(cmd)

'''
for servnum in range(2,73):
    inputfileName = 'data/roller520/roller520synsim.csv'
    outfileName = 'data/roller520/clusters/roller520_' + str(servnum)+ '_cluster.csv'
    cmd = ('python mstClustering.py ' +  inputfileName + '  '  + outfileName + '  ' +  str(servnum) )
    print cmd

    returncode  = subprocess.call(cmd, shell=True)
