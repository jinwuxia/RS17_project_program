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
for servnum in range(1,24):
    inputfileName = 'data/jpetstore6/jpetstore6synsim.csv'
    outfileName = 'data/jpetstore6/jpetstore6_' + str(servnum)+ '_cluster.csv'
    cmd = ('python mstClustering.py ' +  inputfileName + '  '  + outfileName + '  ' +  str(servnum) )
    returncode  = subprocess.call(cmd)
