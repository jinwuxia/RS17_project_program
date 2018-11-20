#analyze cluster metric and extract api
python analyzeCluster.py  traditional_clustering/jwx_wca_uem_WCA_preselected_uem_27_clusters.rsf.csv   workflow/jforum219_workflow_reduced.csv   traditional_clustering/wca_uem_27_clusterAPI.csv
#private cohesion metric
python tosc-interf-dom-cohesion.py
python tosc-interf-msg-cohesion.py


#extract public api
python publicAPI.py  ../testcase_data/jpetstore6/workflow/jpetstore6_testcase_name.csv   ../testcase_data/jpetstore6/traditional_clustering/jwx_wca_uem_WCA_preselected_uem_6_clusters.rsf.csv    ../testcase_data/jpetstore6/traditional_clustering/public_wca_uem_6_clusterAPI.csv
#public cohesion metric
python tosc-interf-dom-cohesion-public.py ...





#######################batch
#get rsf file
getRSF.py    bvn13blogund.csv  bvn13blogund_class_dep.rsf

#class coverage
classstatis.py split/classstatis/*_all_class.txt  ./*und_class_dep.rsf
#move clas_dep to arcade/input

#arcade
cd arcade_0.1.0
#modify .cfg
#wca clutering
java -jar arcade.jar DriverEngine -projfile jwx-cfg/jwx-wca-uem.cfg
# limbo clustering
java -jar arcade.jar DriverEngine -projfile jwx-cfg/jwx-limbo-ilm.cfg

#filter wca and limbo clusters by using class benchmark
python filterOutCluster.py  ../icws2017/data/solo270/solo270_TS_class.csv    ../testcase_data/solo270/traditional_clustering/solo270-limbo/jwx_limbo_ilm_LIMBO_preselected_ilm_10_clusters.rsf.csv   solo270_cluster_10.csv
#generate API for each cluster
batch_analyzeClusterAndAPI.py
#compute cohesion for each api
batch_measure.py

#measure1 by co-change(moran metric)
python cochange_measure1.py  ../testcase_data/solo270/dependency/solo270cmt.csv  ../testcase_data/considerRepeatNot/solo270/limbo/solo270_cluster_10.csv   dddd   > measure_1/solo270_10_limbo.csv

#measure2 by co-change(dmml metric)
python cochange_measure2f.py  jpetstore_service_4_sample.csv(class benchmark)  ../testcase_data/jpetstore6/dependency/jpetstore6cmt.csv   ../../FoME/services/jpetstore/MEM/jpetstore_service_4.csv  ddd
