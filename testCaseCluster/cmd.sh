#!/bin/sh
python reduceWorkflow.py   jforum219_workflow.csv   jforum219_workflow_reduced.csv     jforum219_testCaseName.csv
python ../workflow/workflowTree.py   jforum219_workflow_reduced.csv     longname
mv workflow_longname.tree    jforum219_workflow_reduced_longname.tree
python genTestCaseFv.py  jforum219_workflow_reduced.csv    jforum219_testCaseName.csv   jforum219_workflow_part1.csv    jforum219_testcase_class.csv   jforum219_testcase_fv.csv
python testCaseClustering.py   jforum219_testcase_fv.csv    jm   AVG    3   TS
python analyzeCluster.py     TS_TS_jm_AVG_6.csv    jforum219_testcase_fv.csv   jforum219_testcase_class.csv   mergeCluster.csv
