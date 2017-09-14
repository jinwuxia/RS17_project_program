#!/bin/sh

:<<eof
for((i=40;i>=10;i--));
do
file='../testcase_data/jforum219/coreprocess/jforum219_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/jforum219/coreprocess/jforum219_testcase1_fv.csv    ../testcase_data/jforum219/coreprocess/jforum219_testcase1_class.csv
done
eof

for((i=10;i>=1;i--));
do
file='../testcase_data/jpetstore6/coreprocess/testcaseClustering/jpetstore6_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/jpetstore6/coreprocess/jpetstore6_testcase1_fv.csv    ../testcase_data/jpetstore6/coreprocess/jpetstore6_testcase1_class.csv
#mv 'comb_tmp.txt'   'comb_tmp_'${i}'.txt'
done
