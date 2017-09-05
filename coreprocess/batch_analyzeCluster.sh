#!/bin/sh
for((i=40;i>=30;i--));
do
file='jforum219_jm_AVG_'${i}'.csv'
python ../testCaseCluster/analyzeCluster.py    jforum219  $file    jforum219_testcase1_fv.csv    jforum219_testcase1_class.csv

done
