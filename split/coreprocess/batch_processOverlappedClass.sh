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



step=0.01
scale=2
for ((i=0;i<=100;i++));
do
  cur=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
  file='../testcase_data/jpetstore6/coreprocess/processOverlap/jpetstore6_testcase1_clusters_'${cur}'.csv'
  python coreprocess/processOverlappedClass.py  ../testcase_data/jpetstore6/dependency/jpetstore6_testcase1_mixedDep.csv   ../testcase_data/jpetstore6/dependency/jpetstore6_testcase1_traceDep.csv    ../testcase_data/jpetstore6/coreprocess/testcaseClustering/jpetstore6_testcase1_jm_AVG_4.csv     ../testcase_data/jpetstore6/coreprocess/jpetstore6_testcase1_4_class_nolap.csv    ../testcase_data/jpetstore6/coreprocess/jpetstore6_testcase1_4_class_lap.csv      $file  $cur

  #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
  #echo $cur, $i
  #echo $file
done
