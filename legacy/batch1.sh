#!/bin/sh

dir="/mnt/repo/RS17_apache-tomcat-7.0.78-kk13/logs/"
classname="org.mybatis.jpetstore"
for testsce in "order" "vieworder"
do
    for workload in 10 20 30 40 50 60 70
	do
	    filename="time_"${testsce}"_"${workload}".csv"
		logfile=${dir}${testsce}"_"${workload}
		profile="genTimeStatis.py"
		`python  ${profile}  ${logfile}  ${classname} ${filename}`  
		echo ${filename}
    done 
done
