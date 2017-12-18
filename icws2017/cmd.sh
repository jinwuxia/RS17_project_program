uperl identifierParser.pl jpetstore6.udb  org.mybatis.jpetstore   jpetstore6_words.txt

python semanticParser.py  jpetstore6_words.txt   jpetstore6syn.csv   0.8

python semanticCosin.py  jpetstore6syn.csv   jpetstore6synsim.csv

python mstClustering.py  jpetstore6synsim.csv   jpetstore6clusters.csv  6


python batch_mstClustering.py
python batch_analyzeClusterAndAPI.py  #private

python batch_measure.py roller520  private  private-msg
python batch_measure.py roller520  private  private-dom
python batch_publicAPI.py  #public
