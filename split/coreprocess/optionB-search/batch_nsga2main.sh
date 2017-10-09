project=jpetstore6
for((i=1;i<=30;i++));
do
logfile='../../../testcase_data/'${project}'/coreprocess/optionB-search/'${project}'_nsga_'${i}'.log'
python nsga2main.py  > ${logfile}
echo $logfile
done
