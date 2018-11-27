'''
use all the enum option as popilation, do the preto analysis
then put the first layer's (best set) into file
'''
import sys
import csv
import fastnondomsort
import config
import fitness
import initpop
import csv

FITNESSFILENAME  = config.GlobalVar.FITNESSFILENAME
BIT_COUNT_X = config.GlobalVar.BIT_COUNT_X
BIT_COUNT_Y = config.GlobalVar.BIT_COUNT_Y

def ObjectToStr(oneObject):
    strstr = ''
    strstr += (str(oneObject.servnum) + '_')
    strstr += (str(oneObject.nonlapClassCount) + '_')
    strstr += (str(oneObject.overlapClassCount) + '_')
    strstr += (str(oneObject.realClusterNum) + '_')
    strstr += (str(oneObject.repeatClassCount) + '_')
    strstr += (str(oneObject.interWorklow) + '_')
    strstr += (str(oneObject.withinWorkflow) + '_')
    strstr += (str(oneObject.interCallNum) + '_')
    strstr += (str(oneObject.interCallNum_f) + '_')
    strstr += (str(oneObject.APINum))
    return strstr

#reduce the object_struct_dict
def ReduceRecord(oneDict):
    tmp_dict = dict() #[objectstr] = [serv, thr]
    reduced_object_struct_dict = dict()
    for serv in oneDict:
        for thr_int in oneDict[serv]:
            oneObject = oneDict[serv][thr_int]
            strstr = ObjectToStr(oneObject)
            if strstr not in tmp_dict:  #not duplicated, then add
                tmp_dict[strstr] = [serv, thr_int]
                if serv not in reduced_object_struct_dict:
                    reduced_object_struct_dict[serv] = dict()
                reduced_object_struct_dict[serv][thr_int] = oneObject
            else: #duplicated, then remove the thr_min(previous), add new
                previous_thr_int = tmp_dict[strstr][1]
                tmp_dict[strstr] = [serv, thr_int]
                reduced_object_struct_dict[serv].pop(previous_thr_int)
                reduced_object_struct_dict[serv][thr_int] = oneObject
    return reduced_object_struct_dict

#add all indivs into pop_list, and return real_pop_value
def GenerateIndiv(reduced_object_struct_dict):
    pop_list = list()#[i] = indiv
    real_dict = dict() #[indiv] = [xi, yi]
    for serv in reduced_object_struct_dict:
        for thr_int in reduced_object_struct_dict[serv]:
            xi = serv
            yi = thr_int
            xibit = initpop.Dec2bit(xi, BIT_COUNT_X)
            yibit = initpop.Dec2bit(yi, BIT_COUNT_Y)
            indiv = xibit + yibit
            real_dict[indiv] = [xi, yi]
            pop_list.append(indiv)
    return pop_list, real_dict

#extract bestAnsList
def GenBestAns(firstLayerList,real_dict, reduced_object_struct_dict):
    bestAnsList = list()
    bestAnsList.append(['servnum', 'thr', 'within-service-function counter', \
                    '-repeated-class counter', 'overlapClassCount', \
                    'inter-service-function counter', 'interCallNum',\
                     'APINum',  'realClusterNum'])
    for indiv in firstLayerList:
        xi = real_dict[indiv][0]
        yi = real_dict[indiv][1]
        one = reduced_object_struct_dict[xi][yi]
        bestAnsList.append([one.servnum, yi, one.withinWorkflow, \
                       -one.repeatClassCount, one.overlapClassCount,\
                       one.interWorklow, one.interCallNum, \
                       one.APINum, one.realClusterNum])
    return bestAnsList

#search eachservnum's thr list
def FindServnumBestThr(layerList, real_dict):
    serv2ThrDict = dict()  #[servnum] = [thr list]
    serv2RankDict = dict() #[servnum] = rank  this servnum is in ehich layre
    #change indiv to [xi, yi]
    realLayerList = list() #[0] = [[x,y], []]
    for index in range(0, len(layerList)):
        realLayerList.append(list())
        for indiv in layerList[index]:
            xi = real_dict[indiv][0]
            yi = real_dict[indiv][1]
            realLayerList[index].append([xi,yi])
    for index in range(0, len(realLayerList)):
        for [serv, thr_int] in realLayerList[index]:
            if serv not in serv2ThrDict:
                serv2ThrDict[serv] = list()
                serv2ThrDict[serv].append(thr_int)
                serv2RankDict[serv] = index
            else:
                if serv2RankDict[serv] == index:
                    serv2ThrDict[serv].append(thr_int)
    print 'serv2ThrDict:'
    print  serv2ThrDict
    return serv2ThrDict, serv2RankDict

def GetServnumBestAns(serv2ThrDict, serv2RankDict, reduced_object_struct_dict):
    resultList = list()
    resultList.append(['servnum', 'thr', 'within-service-function counter', \
                    '-repeated-class counter', 'overlapClassCount', \
                    'inter-service-function counter', 'interCallNum',\
                     'APINum',  'realClusterNum', 'pareto-rank'])
    for serv in serv2ThrDict:
        for thr_int in serv2ThrDict[serv]:
            one = reduced_object_struct_dict[serv][thr_int]
            resultList.append([one.servnum, thr_int, one.withinWorkflow, \
                               -one.repeatClassCount, one.overlapClassCount,\
                               one.interWorklow, one.interCallNum, \
                               one.APINum, one.realClusterNum, serv2RankDict[serv]])
    return resultList


def Write2CSV(bestAnsList, outputFileName):
    with open(outputFileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(bestAnsList)
    print 'Finish write ', outputFileName

#python pro.py best_ans_file_name, no/yes
if __name__ == '__main__':
    outputFileName = sys.argv[1]
    repeatFlag = sys.argv[2] # 'no', 'yes'
    if repeatFlag == 'yes':
        #load all fitness value
        fitness.loadFitness(FITNESSFILENAME) #set object_struct_dict
    elif repeatFlag == 'no':
        fitness.loadFitness_noRepeat(FITNESSFILENAME)

    object_struct_dict = config.get_object_struct()
    for serv in object_struct_dict:
        for thr_int in object_struct_dict[serv]:
            one = object_struct_dict[serv][thr_int]
            print serv, thr_int, one.realClusterNum, one.withinWorkflow
    print 'loadFitness finished....\n'

    #Remove the whole same duplicated records
    reduced_object_struct_dict = ReduceRecord(object_struct_dict)
    print 'reduced_object_struct_dict:'
    #print len(reduced_object_struct_dict)
    #coding
    [pop_list, real_dict] = GenerateIndiv(reduced_object_struct_dict)
    # fast non dominate sort
    [layerList, indivRankDict] = fastnondomsort.FastNondomSort(pop_list)

    print 'poplen= ', len(pop_list)
    print 'total layer= ', len(layerList)
    for layerIndex in range(0, len(layerList)):
        print 'layer', layerIndex, 'th length: ', len(layerList[layerIndex]), 'ndiv:', layerList[layerIndex]

    resultList = list()
    resultList.append(['clusternum','thr','servicenumber', 'withinWorkflow' , 'rank'])
    for eachIndiv in indivRankDict:
        rank = indivRankDict[eachIndiv]
        [clusternum, thr] = real_dict[eachIndiv]
        oneObject = reduced_object_struct_dict[clusternum][thr]
        realservicenumber = oneObject.realClusterNum
        withinworkflow = oneObject.withinWorkflow
        thr = int(int(thr) / float(10) + 0.5)
        resultList.append([clusternum, thr, realservicenumber, withinworkflow, rank])
    Write2CSV(resultList, outputFileName)
    #only the first layer
    #bestAnsList = GenBestAns(layerList[0], real_dict, reduced_object_struct_dict)
    #Write2CSV(bestAnsList, outputFileName)

    # for each serv, find its non-dominated(best) answer set
    #[bestServ2ThrDict, serv2RankDict] = FindServnumBestThr(layerList, real_dict)
    #resultList = GetServnumBestAns(bestServ2ThrDict, serv2RankDict, reduced_object_struct_dict)
    #Write2CSV(resultList, outputFileName)
