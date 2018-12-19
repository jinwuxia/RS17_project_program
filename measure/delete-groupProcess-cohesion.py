import os
import subprocess
import sys

if __name__ == '__main__':
    fileType = sys.argv[1]
    from os import walk
    fileList=[]
    for (dirpath, dirnames, filenames) in walk('../testcase_data/repeat3group'):
        for name in filenames:
            if 'clusterAPI' in name:
                f = dirpath + '/' + name
                fileList.append(f)
                print f
    print '\n\n'

    for apiFileName in fileList :
        print apiFileName
        cmd = 'python  tosc-interf-dom-cohesion.py  ' +  apiFileName + ' ' + fileType
        #cmd = 'python  measure/coreprocess/tosc-interf-dom-cohesion.py  ' +  apiFileName
        #cmd = 'python  measure/coreprocess/tosc-interf-msg-cohesion.py  ' +  apiFileName
        returncode  = subprocess.call(cmd, shell=True)
        #print returncode
