#!/bin/sh
#python workflowFilter.py  jforum219_workflow.csv    jforum219_workflow_filter_part_1, part2, part_3
#merge part1 and part3 to be part1

python reduceWorkflow.py   jforum219_workflow.csv   jforum219_workflow_reduced.csv     jforum219_testCaseName.csv
python ../workflow/workflowTree.py   jforum219_workflow_reduced.csv     longname
mv workflow_longname.tree    jforum219_workflow_reduced_longname.tree
#
#
python genTestCaseFv.py  jforum219_workflow_reduced.csv    jforum219_testCaseName.csv   jforum219_workflow_filter_class_part_1.csv    jforum219_testcase_class.csv   jforum219_testcase_fv.csv
python testCaseClustering.py   jforum219_testcase_fv.csv    jm   AVG    3   TS

#
#
python analyzeCluster.py     TS_TS_jm_AVG_4.csv    jforum219_testcase_fv.csv   jforum219_testcase_class.csv   mergeCluster.csv   >  log
#
#
#-----------------------------------根据聚类结果进行结构关系分析--------------
python xmlParser.py  jforum219.xml  jforum219xml.csv
python analyzeStructDeps.py  jforum219xml.csv  jforum219_testcase_class.csv   mergeCluster.csv   split_class_overlap_non.csv   split_class_overlap_high.csv    struct_highoverlap.csv > struct_highoverlap.log
python analyzeStructDeps.py  jforum219xml.csv  jforum219_testcase_class.csv   mergeCluster.csv   split_class_overlap_non.csv   split_class_overlap_low.csv   struct_lowoverlap.csv > struct_lowoverlap.log
#手动拼接上述两个文件，进行分析。


#------------------------------------------------------------------------
#note:
#Q1: workflowFilter
#exclude class 目前是根据自动分层的方法过滤出来的，以及后续发现每个cluster都有的，进行调整的结果。
#    这个已知输入文件需要慎重考虑：
#     方法1: 人为定义需要排出的类或者软件包
#     方法2: 每个workflow的执行流总分总process-》 action-》finally。
#     方法3: 计算所有workflow的交集

#Q2: reduceWorkflow
# test case name生成时，有强编码。

#Q3: 选择那个聚类结果来分析，则需要慎重挑选

#Q4: analyzeCluster
#    决定 high-overlap, low-ovelap 时设置了阈值。
#--------------------------------------------------------------------------
