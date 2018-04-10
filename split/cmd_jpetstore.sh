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
git bracn -a # view all branchs
git checkout -b BRACHNAME   origin/BRACNNAME # switch to this branch
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
python ../../../split/dependency/mixParser.py    ${project}xml.csv   null ${project}com.csv   ../coreprocess/${project}_testcase1_class.csv   ${project}_testcase1_mixedDep.csv



#python  ${code_core_dir}analyzeOneCluster.py  testcaseClustering/${project}_testcase1_jm_AVG_4.csv   ${project}_testcase1_fv.csv   ${project}_testcase1_class.csv   ${project}_testcase1_4_class_nolap.csv  ${project}_testcase1_4_class_lap.csv     ${project}_testcase1_4_classclusterFv.csv
#python ../../coreprocess/traceParser.py  coreprocess/jforum219_testcase1_20_classclusterFv.csv    dependency/jforum219_testcase1_traceDep.csv
#in linux:   ./batch_processOverlap.sh
#in linux: ./batch_analyzeProcessOverlapRes.sh > log.csv


#enum lapclass, nonlap class, all thr and servers' custer result
cd coreprocess/optionA-enum
python enum.py project_fitness.csv

#pareto anaysis all possible answers, fitness.loadFitness_noRepeat
cd optionB-search
#use loadFitness_noRepeat
python paretoanalysis.py    ../../../testcase_data/jpetstore6/coreprocess/jpetstore6_pareto_analysis_servnum_best_norepeat.csv  no
#use loadFitness()
python paretoanalysis.py    ../../../testcase_data/jpetstore6/coreprocess/jpetstore6_pareto_analysis_servnum_best.csv    yes

#according to above pareto analysis result, choose a proper real service number, then produce its api
#modify batch_getcomponentAPI.py, get compoennt API.
python batch_getcomponentAPI.py

#or extract ProReqAPI
#for icws, limbo, wca
python ../../icws2017/getComponentProReqAPI.py  \
jpetstore6/limbo/jwx_limbo_ilm_LIMBO_preselected_ilm_4_clusters.rsf.csv  \
../jpetstore6/workflow/jpetstore6_workflow_reduced.csv  \
jpetstore6/limbo/jpetstore6_4_clusterProReqAPI.csv


#-----------------------------------------------
#generate all  componentAPI
#in linux: ./batch_getcomponentAPI.sh

'''
#coreprocess automaticlaly decide the servernum and thr using NSGAII
cd coreprocess/optionB-search
python nsga2main.py   jpetstore6_nsga.csv   jpetstore6_nsga_best.csv #set parameter in config.py

#compare with random
#python randmaim.py jpetstore6_randall.csv


#use the nsga average as the result, then analsis jpetstore6_nsga.csv
#interface, api,peravg
'''

#measurement cohesion and coupling         public vs private
python tosc-interd-msg-cohesion.py   servnum-thr-clusterAPI.csv
python tosc-interd-dom-cohesion.py   servnum-thr-clusterAPI.csv
#python tosc-interd-dom-cohesion-public .py   testcasecluster.csv

#measure our proposed metric by co-change benchmark
measure/cochange_measure1.py   
measure/cochange_measure2f.py  #biased, not use

#icws process, refer to icws/cmd.sh
#wca,limbo process, refer to traditionalClustering/cmd.sh


# statatis trace data, commit data, trace-to-trace simlarity



-------------------------------------------------------------------REFER TO CMD.SH
#------------------------------------------------
#get testcase_all_calss.csv

#get all class(using understrand)

#get no_ts_cover_class(not include dao,view) and testcase_common_class(not include dao,view)



#-------------------------------------------------
#process testcase_common_class :    or not process:  only one cluster


#function-core class merged into existing clusters using struct dep


#other unprocessed no-ts-cover-class clustering inside using struct dep(beacuse commDep = 0, no-cover)
