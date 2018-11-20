uperl identifierParser.pl jpetstore6.udb  org.mybatis.jpetstore   jpetstore6_words.txt

python semanticParser.py  jpetstore6_words.txt   jpetstore6syn.csv   

python semanticCosin.py  jpetstore6syn.csv   jpetstore6synsim.csv

#count the coverage when use different   sim threshold
python classstatis.py   jpetstore6_all_class.csv   jpetstore6synsim.csv

#use class benchmark to filter the sim file
python semanticFilter.py classFile   jpetstore6synsim.csv  after_filter_jpetstore6synsim.csv
python mstClustering.py  after_filter_jpetstore6synsim.csv   jpetstore6clusters.csv  6


python batch_mstClustering.py
python batch_analyzeClusterAndAPI.py  #private

python batch_measure.py roller520  private  private-msg
python batch_measure.py roller520  private  private-dom
python batch_publicAPI.py  #public
