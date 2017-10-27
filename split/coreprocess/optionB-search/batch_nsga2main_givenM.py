import sys
import os
import subprocess
#python pr.py data_dir projec
if __name__ == '__main__':
    data_dir = sys.argv[1]
    project = sys.argv[2]

    for M in range(2,3):  #M is variable TS cluster number

        #modify config
        fp = open("config.py", "r+")
        flist = fp.readlines()
        flist[7] = ('    X_S = ' + str(M) + '\n')
        flist[8] = ('    X_E = ' + str(M) + '\n')
        flist[9] =  '    BIT_COUNT_X = 0\n'

        fp = open("config.py", "w+")
        fp.writelines(flist)
        fp.close()
        
        # run nsgamain
        allfile = ('../../../testcase_data/' + data_dir \
                  + '/coreprocess/optionB-search/givenM/' \
                  + project + '_nsga_' + str(M) + '_all.csv')
        bestfile =('../../../testcase_data/' + data_dir \
                  + '/coreprocess/optionB-search/givenM/'\
                  + project + '_nsga_' + str(M) + '_best.csv')

        #python nsga2main.py $allfile $bestfile
        cmd = ("python nsga2main.py  " + allfile + "  " + bestfile )
        returnCode = subprocess.call(cmd)
        print 'returnCode: ', returnCode
