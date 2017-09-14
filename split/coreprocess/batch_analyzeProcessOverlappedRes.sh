#!/bin/bash
#project='jforum219'
#num=20
project='jpetstore6'
num='4'
step=0.01
scale=2
for ((i=0;i<=100;i++));
do
  cur=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
  arg1_file='../testcase_data/'${project}'/coreprocess/processOverlap/'${project}'_testcase1_clusters_'${cur}'.csv'
  arg2_file='../testcase_data/'${project}'/coreprocess/testcaseClustering/'${project}'_testcase1_jm_AVG_'${num}'.csv'
  arg3_file='../testcase_data/'${project}'/workflow/'${project}'_workflow_reduced.csv'
  echo $cur, `python coreprocess/analyzeProcessOverlapRes.py $arg1_file $arg2_file $arg3_file`

  #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
  #echo $file
done
