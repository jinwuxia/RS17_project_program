project='jpetstore6'
filter='org.mybatis'

cd testcase_data/${project}/workflow
code_workflow_dir='../../../split/workflow/'
python ${code_workflow_dir}traceWorkflow.py  ../../../../RS17_source_data/RS17_${project}/dynamic/log   ${project}_workflow.csv  $filter
python ${code_workflow_dir}workflowTree.py   ${project}_workflow.csv longname  ${project}_workflow_longname.tree

python  ${code_workflow_dir}reduceWorkflow.py  ${project}_workflow.csv   ${project}_workflow_reduced.csv  ${project}_testcase_name.csv
python  ${code_workflow_dir}workflowTree.py   ${project}_workflow_reduced.csv   longname  ${project}_workflow_reduced_longname.tree


cd testcase_data/${project}/dependency
code_depend_dir='../../../split/dependency/'
git log --name-status > ../testcase_data/jforum219/dependency/jforum219.gitlog
#manual: delete update.init commit log
und export -dependencies class cytoscape ${project}.xml  ${project}.udb
python ${code_depend_dir}xmlParser.py  ${project}.xml   ${project}xml.csv
python ${code_depend_dir}cmtParser.py  ${project}.gitlog   ${project}cmt.csv  java
python ${code_depend_dir}comParser.py  ../workflow/${project}_workflow_reduced.csv   ${project}com.csv

cd testcase_data/${project}/coreprocess
code_core_dir='../../../split/coreprocess/'
python ${code_core_dir}genTestCaseFv.py  ../workflow/${project}_workflow_reduced.csv   ../workflow/${project}_testcase_name.csv  null  ${project}_testcase0_in_entity.csv     ${project}_testcase0_class.csv  ${project}_testcase0_fv.csv
python ${code_core_dir}testCaseClusteringByEntity.py   ${project}_testcase0_fv.csv   ${project}_testcase0_clusters.csv


python  ${code_core_dir}genTestCaseFv.py  ../workflow/${project}_workflow_reduced.csv   ../workflow/${project}_testcase_name.csv  ${project}_testcase1_ex_actdao.csv  null ${project}_testcase1_class.csv  ${project}_testcase1_fv.csv
python  ${code_core_dir}testCaseClustering.py   ${project}_testcase1_fv.csv    ${project}_testcase0_clusters.csv  jm AVG  1  ${project} 0.01
mkdir testCaseClustering
mv ${project}_testcase1_jm_AVG_*   testCaseClustering/

./coreprocess/batch_analyzeCluster.sh  > log.csv
python  ${code_core_dir}analyzeOneCluster.py  testcaseClustering/${project}_testcase1_jm_AVG_4.csv   ${project}_testcase1_fv.csv   ${project}_testcase1_class.csv   ${project}_testcase1_4_class_nolap.csv  ${project}_testcase1_4_class_lap.csv     ${project}_testcase1_4_classclusterFv.csv

python ../../../split/dependency/mixParser.py    ${project}xml.csv   null ${project}com.csv   ../coreprocess/${project}_testcase1_class.csv   ${project}_testcase1_mixedDep.csv
python ../../coreprocess/traceParser.py  coreprocess/jforum219_testcase1_20_classclusterFv.csv    dependency/jforum219_testcase1_traceDep.csv

in linux:   ./batch_processOverlap.sh
in linux: ./batch_analyzeProcessOverlapRes.sh > log.csv
