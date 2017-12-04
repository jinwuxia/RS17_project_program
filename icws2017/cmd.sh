uperl identifierParser.pl jpetstoe6.udb  org.mybatis.jpetstore   jpetstore6_words.txt

python semanticParser.py  jpetstore6_words.txt   jpetstore6syn.csv   0.9

python semanticCosin.py  jpetstore6syn.csv   jpetstore6synsim.csv

python mstClustering.py  jpetstore6synsim.csv   jpetstore6clusters.csv  6
