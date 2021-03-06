#!/bin/sh

:<<eof
for((i=40;i>=10;i--));
do
file='../testcase_data/jforum219/coreprocess/jforum219_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/jforum219/coreprocess/jforum219_testcase1_fv.csv    ../testcase_data/jforum219/coreprocess/jforum219_testcase1_class.csv
done
eof

:<<eof
project=jforum219
cluster_num=47
for((i=${cluster_num};i>=1;i--));
do
file='../testcase_data/jforum219_1/coreprocess/testcaseClustering/'${project}'_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/jforum219_1/coreprocess/${project}_testcase1_fv.csv    ../testcase_data/${project}_1/coreprocess/${project}_testcase1_class.csv
#mv 'comb_tmp.txt'   'comb_tmp_'${i}'.txt'
done
eof


:<<eof
#roller
project=roller520
cluster_num=72
for((i=${cluster_num};i>=7;i--));
do
file='../testcase_data/'${project}'/coreprocess/testcaseClustering/'${project}'_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/${project}/coreprocess/${project}_testcase1_fv.csv    ../testcase_data/${project}/coreprocess/${project}_testcase1_class.csv
#mv 'comb_tmp.txt'   'comb_tmp_'${i}'.txt'
done
eof

:<<eof
#bvn13
project=bvn13
cluster_num=26
for((i=${cluster_num};i>=1;i--));
do
file='../testcase_data/'${project}'/coreprocess/testcaseClustering/'${project}'_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/${project}/coreprocess/${project}_testcase1_fv.csv    ../testcase_data/${project}/coreprocess/${project}_testcase1_class.csv
#mv 'comb_tmp.txt'   'comb_tmp_'${i}'.txt'
done
eof

:<<eof
#solo270
project=solo270
cluster_num=70
for((i=${cluster_num};i>=2;i--));
do
file='../testcase_data/'${project}'/coreprocess/testcaseClustering/'${project}'_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/${project}/coreprocess/${project}_testcase1_fv.csv    ../testcase_data/${project}/coreprocess/${project}_testcase1_class.csv
#mv 'comb_tmp.txt'   'comb_tmp_'${i}'.txt'
done
eof

#xwiki-platform
project=xwiki-platform108
cluster_num=300
for((i=${cluster_num};i>=50;i--));
do
file='../testcase_data/'${project}'/coreprocess/testcaseClustering/'${project}'_testcase1_jm_AVG_'${i}'.csv'
python coreprocess/analyzeAllCluster.py   $file    ../testcase_data/${project}/coreprocess/${project}_testcase1_fv.csv    ../testcase_data/${project}/coreprocess/${project}_testcase1_class.csv
#mv 'comb_tmp.txt'   'comb_tmp_'${i}'.txt'
done
