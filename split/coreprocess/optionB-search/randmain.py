'''
random choose pop, aim for comparing with nsga2
'''

import csv
import sys
import config
import initpop
import fitness

N = 12 #initial populization size, each generation size = intialSize
X_S = config.GlobalVar.X_S
X_E = config.GlobalVar.X_E
Y_S = config.GlobalVar.Y_S
Y_E = config.GlobalVar.Y_E
BIT_COUNT_X = config.GlobalVar.BIT_COUNT_X
BIT_COUNT_Y = config.GlobalVar.BIT_COUNT_Y
FITNESSFILENAME = config.GlobalVar.FITNESSFILENAME
FITNESS_METHOD_LIST = config.GlobalVar.FITNESS_METHOD_LIST


def Write2CSV(listlist, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)
    print fileName

if __name__ == '__main__':
    allFileName =  sys.argv[1]
    bestFileName = sys.argv[2]

    fitness.loadFitness(FITNESSFILENAME) #set OBJECT_STRUCT_DICT
    OBJECT_STRUCT_DICT = config.get_object_struct()
    for serv in OBJECT_STRUCT_DICT:
        for thr_int in OBJECT_STRUCT_DICT[serv]:
            one = OBJECT_STRUCT_DICT[serv][thr_int]
            #print serv, thr_int, one.nonlapClassCount, one.nonlapClassCount_avg, one.withinWorkflow, one.interWorklow, one.APINum, one.APINum_avg
    #print 'loadFitness finished....\n'

    all_result_list = list()
    best_fitness_list = list() #[]= [withinWorkflow , -repeat, clusternum] 30times
    for i in range (0, 30):
        pop_list = initpop.InitPop(N, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)

        best_cluster_tmp = list()
        best_repeat_tmp = list()
        best_within_tmp = list()
        for indiv in pop_list:
            [xi, yi] = initpop.TransCode2Indiv(indiv, BIT_COUNT_X, BIT_COUNT_Y)
            one = OBJECT_STRUCT_DICT[xi][yi]
            '''
            strstr = str(xi) + ',' + str(yi) + ',' \
            + str(one.overlapClassCount) + ',' \
            + str(one.withinWorkflow) + ',' \
            + str(one.interWorklow) + ',' \
            + str(one.interCallNum) + ',' \
            + str(one.repeatClassCount) + ',' \
            + str(one.APINum)
            '''

            all_result_list.append([xi, yi, one.overlapClassCount, one.withinWorkflow, one.interWorklow, one.interCallNum, one.repeatClassCount, one.APINum])

            best_within_tmp.append(one.withinWorkflow)
            best_repeat_tmp.append(-one.repeatClassCount)
            best_cluster_tmp.append(one.realClusterNum)

        within = sum(best_within_tmp) / len(best_within_tmp)
        repeat = sum(best_repeat_tmp) / len(best_repeat_tmp)
        cluster = sum(best_cluster_tmp) / len(best_cluster_tmp)
        best_fitness_list.append([within, repeat, cluster])

    #save to csv
    Write2CSV(all_result_list, allFileName)
    Write2CSV(best_fitness_list, bestFileName)
