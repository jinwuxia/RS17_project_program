import sys
import subprocess
import time
#jpetstore 3 3 6   30  8
# expect_unbuffer python3 test.py  3   10  50 20  springblog   > run_springblog.txt  &
#solo270  5  20   40 20
#jforum219 5  20  40 20


start = int(sys.argv[1])
end = int(sys.argv[2])
pop_size = sys.argv[3]
parent_size = sys.argv[4]
project = sys.argv[5]
coverage = sys.argv[6]

for M in range(start, end + 1):

    #modify config
    fp = open("msconfig.py", "r+")
    flist = fp.readlines()
    flist[15] = ('    POP_SIZE = ' + pop_size + '\n')
    flist[16] = ('    PARTITION_K = ' + str(M) + '\n')
    flist[17] = ('    PARENT_M = ' + parent_size + '\n')

    fp = open("msconfig.py", "w+")
    fp.writelines(flist)
    fp.close()

    groupfile = "../testcase_data/improvement/groupclassresult/" + project + "_2_" + coverage + ".csv"
    calldepFile = "../testcase_data/improvement/calldep/" + project + "_calldep_"  + coverage + ".csv"
    concerndepFile = "../testcase_data/improvement/concerndep/" + project + "_concerndep.csv"
    logfile = project + "_" + str(M) + "_" + coverage + "_log.csv"

    cmd = ("python main.py " + groupfile + " "
              + calldepFile + " " + concerndepFile + " "
              + project +  "  " + logfile)
    print(cmd)


    returncode  = subprocess.call(cmd, shell=True)
    time.sleep(10)
