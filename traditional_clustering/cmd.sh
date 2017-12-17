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
getRSF.py
# limbo clustering
arcade
# wca clustering
arcade
#generate API for each cluster
batch_analyzeClusterAndAPI.py
#compute cohesion for each api
batch_measure.py
