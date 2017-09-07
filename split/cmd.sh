#!/bin/sh
cd testcase_data
mkdir jforum219
mkdir jforum219/workflow
mkdir jforum219/dependency


cd ../../RS17_project_program/workflow
#generate workflow.csv from kiekerlogfile
python traceWorkflow.py  ../jforumlogFileDir    ../testcase_data/jforum219/workflow/jforum219_workflow.csv    net.jforum
#filter part1, part2 and part3
python workflowFilter.py  ../testcase_data/jforum219/workflow/jforum219_workflow.csv    ../testcase_data/jforum219/workflow/jforum219_workflow_part1.csv  ../testcase_data/jforum219/workflow/jforum219_workflow_part2.csv ../testcase_data/jforum219/workflow/jforum219_workflow_part3.csv
#manual:     merge part1 and part3 to be part1. part2 adjust
#generate testcaseName and reduced_workflow
python reduceWorkflow.py   ../testcase_data/jforum219/workflow/jforum219_workflow.csv   ../testcase_data/jforum219/workflow/jforum219_workflow_reduced.csv     ../testcase_data/jforum219/workflow/jforum219_testcase_name.csv
python workflowTree.py   ../testcase_data/jforum219/workflow/jforum219_workflow_reduced.csv     longname    ../testcase_data/jforum219/workflow/jforum219_workflow_reduced_longname.tree
python workflowTree.py   ../testcase_data/jforum219/workflow/jforum219_workflow_reduced.csv     shortname   ../testcase_data/jforum219/workflow/jforum219_workflow_reduced_shortname.tree


#generate struct, commit, commun dependency between classes
cd ../../RS17_project_program/dependency
git log --name-status > ../testcase_data/jforum219/dependency/jforum219.gitlog   #显示新增、修改、删除的文件清单
python xmlParser.py  ../testcase_data/jforum219/dependency/jforum219.xml     ../testcase_data/jforum219/dependency/jforum219xml.csv
python cmtParser.py  ../testcase_data/jforum219/dependency/jforum219.gitlog     ../testcase_data/jforum219/dependency/jforum219cmt.csv  java
python comParser.py ../testcase_data/jforum219/workflow/jforum219_workflow_reduced.csv   ../testcase_data/jforum219/dependency/jforum219com.csv


#do testcase clutering by core_function_entity (entity class in part2)
cd testcase_data/jforum219
#manul: generate  coreprocess/jforum219_testcase0_in_entity.csv (can  be class or package.*)
python ../../coreprocess/genTestCaseFv.py  workflow/jforum219_workflow_reduced.csv   workflow/jforum219_testcase_name.csv   null  coreprocess/jforum219_testcase0_in_entity.csv  coreprocess/jforum219_testcase0_class.csv  coreprocess/jforum219_testcase0_fv.csv
python ../../coreprocess/testCaseClusteringByEntity.py   coreprocess/jforum219_testcase0_fv.csv coreprocess/jforum219_testcase0_clusters.csv


#do testcase clusteing by core_function_class(all class in part2)
#manul: generate  coreprocess/jforum219_testcase1_in_class.csv (can  be class or package.*)
cp  workflow/jform219_workflow_part2.csv   coreprocess/jforum219testcase1_in.csv
#####python   ../../coreprocess/genTestCaseFv.py  workflow/jforum219_workflow_reduced.csv  workflow/jforum219_testcase_name.csv   null  coreprocess/jforum219_testcase1_in.csv   coreprocess/jforum219_testcase1_class.csv   coreprocess/jforum219_testcase1_fv.csv
python   ../../coreprocess/genTestCaseFv.py  workflow/jforum219_workflow_reduced.csv  workflow/jforum219_testcase_name.csv  coreprocess/jforum219_testcase1_ex_actdao.csv  null   coreprocess/jforum219_testcase1_class.csv   coreprocess/jforum219_testcase1_fv.csv
python ../../coreprocess/testCaseClustering.py   coreprocess/jforum219_testcase1_fv.csv    coreprocess/jforum219_testcase0_clusters.csv   jm  AVG  1  jforum219   0.01
mv jforum219_testcase1_*  coreprocess/


#analyze which jforum219_testcase1_cluster is best
cd split
coreprocess/batch_analyzeCluster.sh > log.csv
#maunal: merge log.csv and simcvalue.csv , draw line

#analyze the best_num clusters,generate  non-verlapp and overlap file, and class-cluster-fv  file
cd testcase_data/jforum219
python ../../coreprocess/analyzeOneCluster.py  coreprocess/jforum219_testcase1_jm_AVG_20.csv  coreprocess/jforum219_testcase1_fv.csv  coreprocess/jforum219_testcase1_class.csv  coreprocess/testcase1_20_class_nolap.csv  coreprocess/jforum219_testcase1_20_class_lap.csv     coreprocess/jforum219_testcase1_20_classclusterFv.csv


#process overlapped core_function_class
cd testcase_data/jforum219
#generate mixDep
python ../../coreprocess/mixParser.py   dependency/jforum219xml.csv   null  dependency/jforum219com.csv  coreprocess/jforum219_testcase1_class.csv  coreprocess/jforum219_testcase1_mixedDep.csv
#generate traceDep
python ../../coreprocess/traceParser.py  coreprocess/jforum219_testcase1_20_classclusterFv.csv    dependency/jforum219_testcase1_traceDep.csv
#process overlapped class
python ../../coreprocess/processOverlappedClass.py  dependency/jforum219_testcase1_mixedDep.csv    dependency/jforum219_testcase1_traceDep.csv  coreprocess/jforum219_testcase1_class_overlap_no_20.csv    coreprocess/jforum219_testcase1_class_overlap_20.csv    ../testCaseCluster_1/jforum219_cluster_2.csv


#do class clutering for other_non_core_class
python ../../coreprocess/mixParser.py   dependency/jforum219xml.csv   null  dependency/jforum219com.csv  null  dependency/jforum219TotalDep.csv


python  processOtherClass.py    jforum219TotalDep.csv      ../testCaseCluster_1/jforum219_testcase_class_1.csv     ../testCaseCluster_1/jforum219_testcase_class_all.csv   hehe.csv
















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



#-----------------------------------根据聚类结果进行通信代价分析--------------
python comParser.py   jforum219_workflow_reduced.csv     jforum219com.csv
python analyzeComDeps.py   jforum219com.csv  jforum219_testcase_class.csv   mergeCluster.csv  split_class_overlap_non.csv    split_class_overlap_high.csv    com_highoverlap.csv     >  com_highoverlap.log
python analyzeComDeps.py   jforum219com.csv  jforum219_testcase_class.csv   mergeCluster.csv  split_class_overlap_non.csv    split_class_overlap_low.csv    com_lowoverlap.csv     >  com_lowoverlap.log



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
