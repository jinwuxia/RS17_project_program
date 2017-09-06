#!/bin/sh

for testsce in "viewcategory" "search" "order" "vieworder"
do 
    for workload in 10 20 30 40 50 60 70
    do
	testplanfile="testplan_"${testsce}"_"${workload}".jmx"
	testresfile="testres_"${testsce}"_"${workload}".jtl"
	
	echo "execute: "$testplanfile
	#execute ans save testresult
	cd /e/share-experiments/gitrepo/RS17_source_data/RS17_jpetstore6/dynamic/testscript
	/e/share-experiments/gitrepo/apache-jmeter-3.1/bin/jmeter -n -t $testplanfile -l $testresfile
	echo "finish: "$testplanfile

	#save kiekerlog
	kiekerfile="/e/share-experiments/gitrepo/RS17_apache-tomcat-7.0.78-kk13/logs/"${testsce}"_"${workload}
	echo "copy: "$kiekerfile
        cp -r /e/share-experiments/gitrepo/RS17_apache-tomcat-7.0.78-kk13/logs/kiekerlog  $kiekerfile
	echo "finish copying: "$kiekerfile

	sleep 10s
	
    done
done
