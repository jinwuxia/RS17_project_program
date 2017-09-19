#!/bin/bash
:<<eof
step=0.01
scale=2
for ((i=0;i<=100;i++));
do
  cur=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
  file='../testcase_data/jforum219/coreprocess/processOverlap1/jforum219_testcase1_clusters_'${cur}'.csv'
  python coreprocess/processOverlappedClass.py  ../testcase_data/jforum219/dependency/jforum219_testcase1_mixedDep.csv   ../testcase_data/jforum219/dependency/jforum219_testcase1_traceDep.csv    ../testcase_data/jforum219/coreprocess/testcaseClustering/jforum219_testcase1_jm_AVG_20.csv     ../testcase_data/jforum219/coreprocess/jforum219_testcase1_20_class_nolap.csv    ../testcase_data/jforum219/coreprocess/jforum219_testcase1_20_class_lap.csv      $file  $cur

  #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
  #echo $cur, $i
  #echo $file
done
eof


project=jforum219
step=0.01
scale=2
for ((i=0;i<=100;i++));
do
  cur=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
  file='../testcase_data/jforum219_1/coreprocess/processOverlap/'${project}'_testcase1_clusters_'${cur}'.csv'
  python coreprocess/processOverlappedClass.py  ../testcase_data/jforum219_1/dependency/${project}_testcase1_mixedDep.csv   ../testcase_data/jforum219_1/dependency/${project}_testcase1_traceDep.csv    ../testcase_data/jforum219_1/coreprocess/testcaseClustering/${project}_testcase1_jm_AVG_28.csv     ../testcase_data/jforum219_1/coreprocess/${project}_testcase1_28_class_nolap.csv    ../testcase_data/jforum219_1/coreprocess/${project}_testcase1_28_class_lap.csv      $file  $cur

  #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
  #echo $cur, $i
  #echo $file
done
