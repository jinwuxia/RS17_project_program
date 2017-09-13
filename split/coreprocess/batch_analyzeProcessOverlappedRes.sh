#!/bin/bash

step=0.01
scale=2
for ((i=0;i<=100;i++));
do
  cur=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
  arg1_file='../testcase_data/jforum219/coreprocess/processOverlap1/jforum219_testcase1_clusters_'${cur}'.csv'
  arg2_file='../testcase_data/jforum219/coreprocess/testcaseClustering/jforum219_testcase1_jm_AVG_20.csv'
  arg3_file='../testcase_data/jforum219/workflow/jforum219_workflow_reduced.csv'
  echo $cur, `python coreprocess/analyzeProcessOverlapRes.py $arg1_file $arg2_file $arg3_file`

  #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
  #echo $file
done
