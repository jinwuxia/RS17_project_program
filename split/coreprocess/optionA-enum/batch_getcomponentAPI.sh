#!/bin/bash

:<<eof
thrclusterdir=../../../testcase_data/jpetstore6/coreprocess/optionA-enum/
servclusterdir=../../../testcase_data/jpetstore6/coreprocess/testcaseClustering/
workflowfile=../../../testcase_data/jpetstore6/workflow/jpetstore6_workflow_reduced.csv
outdir=../../../testcase_data/jpetstore6/coreprocess/optionA-enum/
project=jpetstore6
step=0.01
scale=2
for ((i=50;i<=100;i++))
do
  for ((serv=3;serv<=4;serv++))
  do
    thr=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
    python ../getComponentAPI.py  ${thrclusterdir}${project}_testcase1_clusters_${serv}_${thr}.csv  ${servclusterdir}${project}_testcase1_jm_AVG_${serv}.csv  ${workflowfile}    ${outdir}${project}_testcase1_${serv}_${thr}_clustersAPI.csv

    #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
    echo $i, $serv
    #echo $file
  done
done
eof



:<<eof
thrclusterdir=../../../testcase_data/jforum219_1/coreprocess/optionA-enum/
servclusterdir=../../../testcase_data/jforum219_1/coreprocess/testcaseClustering/
workflowfile=../../../testcase_data/jforum219_1/workflow/jforum219_workflow_reduced.csv
outdir=../../../testcase_data/jforum219_1/coreprocess/optionA-enum/
project=jforum219
step=0.01
scale=2
for ((i=50;i<=100;i++))
do
  for ((serv=20;serv<=30;serv++))
  do
    thr=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
    python ../getComponentAPI.py  ${thrclusterdir}${project}_testcase1_clusters_${serv}_${thr}.csv  ${servclusterdir}${project}_testcase1_jm_AVG_${serv}.csv  ${workflowfile}    ${outdir}${project}_testcase1_${serv}_${thr}_clustersAPI.csv

    #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
    echo $i, $serv
    #echo $file
  done
done
eof


thrclusterdir=../../../testcase_data/roller520/coreprocess/optionA-enum/
servclusterdir=../../../testcase_data/roller520/coreprocess/testcaseClustering/
workflowfile=../../../testcase_data/roller520/workflow/roller520_workflow_reduced.csv
outdir=../../../testcase_data/roller520/coreprocess/optionA-enum/
project=roller520
step=0.01
scale=2
for ((i=1;i<=100;i++))
do
  for ((serv=7;serv<=72;serv++))
  do
    thr=`echo "1 - $step * $i" | bc | awk '{printf "%.2f", $0}'`
    python ../getComponentAPI.py  ${thrclusterdir}${project}_testcase1_clusters_${serv}_${thr}.csv  ${servclusterdir}${project}_testcase1_jm_AVG_${serv}.csv  ${workflowfile}    ${outdir}${project}_testcase1_${serv}_${thr}_clustersAPI.csv

    #echo "scale=2; 0.13 + 0.1" | bc | awk '{printf "%.2f", $0}'
    echo $i, $serv
    #echo $file
  done
done
