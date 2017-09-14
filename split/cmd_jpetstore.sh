cd testcase_data/jpetstore6/workflow
python ../../../split/workflow/traceWorkflow.py  ../../../../RS17_source_data/RS17_jpetstore6/dynamic/log   jpetstore6_workflow.csv   org.mybatis
python ../../../split/workflow/workflowTree.py   jpetstore6_workflow.csv longname  jpetstore6_workflow_longname.tree

python ../../../split/workflow/reduceWorkflow.py  jpetstore6_workflow.csv   jpetstore6_workflow_reduced.csv  jpetstore6_testcase_name.csv
python ../../../split/workflow/workflowTree.py   jpetstore6_workflow_reduced.csv   longname  jpetstore6_workflow_reduced_longname.tree


cd testcase_data/jpetstore6/dependency
git log --name-status > ../testcase_data/jforum219/dependency/jforum219.gitlog
#manual: delete update.init commit log
und export -dependencies class cytoscape jpetstore6.xml  jpetstore6.udb
python ../../../split/dependency/xmlParser.py  jpetstore6.xml   jpetstore6xml.csv
python ../../../split/dependency/cmtParser.py  jpetstore6.gitlog   jpetstore6cmt.csv  java
python ../../../split/dependency/comParser.py  ../workflow/jpetstore6_workflow_reduced.csv   jpetstore6com.csv


python ../../../split/coreprocess/genTestCaseFv.py  ../workflow/jpetstore6_workflow_reduced.csv   ../workflow/jpetstore6_testcase_name.csv  null  jpetstore6_testcase0_in_entity.csv     jpetstore6_testcase0_class.csv  jpetstore6_testcase0_fv.csv
python ../../../split/coreprocess/testCaseClusteringByEntity.py   jpetstore6_testcase0_fv.csv   jpetstore6_testcase0_clusters.csv


python ../../../split/coreprocess/genTestCaseFv.py  ../workflow/jpetstore6_workflow_reduced.csv   ../workflow/jpetstore6_testcase_name.csv  jpetstore6_testcase1_ex_actdao.csv  null jpetstore6_testcase1_class.csv  jpetstore6_testcase1_fv.csv
python ../../../split/coreprocess/testCaseClustering.py   jpetstore6_testcase1_fv.csv    jpetstore6_testcase0_clusters.csv  jm AVG  1  jpetstore6 0.01
mkdir testCaseClustering
mv jpetstore6_testcase1_jm_AVG_*   testCaseClustering/

./coreprocess/batch_analyzeCluster.sh  > log.csv
python ../../../split/coreprocess/analyzeOneCluster.py  testcaseClustering/jpetstore6_testcase1_jm_AVG_4.csv   jpetstore6_testcase1_fv.csv   jpetstore6_testcase1_class.csv   jpetstore6_testcase1_4_class_nolap.csv  jpetstore6_testcase1_4_class_lap.csv     jpetstore6_testcase1_4_classclusterFv.csv
