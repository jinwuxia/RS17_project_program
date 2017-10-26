#1/bin/sh
project=jpetstore6
configfile=config.py

for((M=2;M<=2;M++));
do
sed -n '8p' $configfile
sed -n '9p' $configfile
sed -n '10p' $configfile

#substituate config.py line 8,9,10 to specify X=M
sed -n '/X_S=[0-9][0-9]*#/p'   config.py | sed  "s/X_S=[0-9][0-9]*#/X_S=${M}/g"      $configfile   > tmp1.py
sed -n '/X_E=[0-9][0-9]*#/p'   tmp1.py  | sed  "s/X_E=[0-9][0-9]*#/X_E=${M}/g"      tmp1.py   > tmp2.py
sed -n '/BIT_COUNT_X=[0-9][0-9]*#/p' tmp2.py | sed "s/BIT_COUNT_X=[0-9][0-9]*#/BIT_COUNT_X=0/g" tmp2.py > tmp3.py
rm tmp1.py
rm tmp2.py


sed -n "9s/=\[0-9\]\+/=$M/"  ${configfile}
sed -n "10s/BIT_COUNT_X=[0-9]+/BIT_COUNT_X=0/"  ${configfile}

sed -n '8p' $configfile
sed -n '9p' $configfile
sed -n '10p' $configfile
allfile='../../../testcase_data/'${project}'/coreprocess/optionB-search/givenM/'${project}'_nsga_'${M}'_all.csv'
bestfile='../../../testcase_data/'${project}'/coreprocess/optionB-search/givenM/'${project}'_nsga_'${M}'_best.csv'
#python nsga2main.py $allfile $bestfile
echo $allfile
echo $bestfile
done
