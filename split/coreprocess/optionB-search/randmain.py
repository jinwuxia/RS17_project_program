'''
random choose pop, aim for comparing with nsga2
'''

import csv
import sys
import config
import initpop
import fitness

#for jpetstore6
X_S = 2#3 #2
X_E = 10 #4 #10
BIT_COUNT_X = 4
BIT_COUNT_Y = 7
FITNESSFILENAME = '../../../testcase_data/jpetstore6/coreprocess/jpetstore6-fitness.csv'
'''
#for jforum219_1
X_S = 18 #20 #18
X_E = 47 #30 #47
BIT_COUNT_X = 6
BIT_COUNT_Y = 7
FITNESSFILENAME = '../../../testcase_data/jforum219_1/coreprocess/jforum219-fitness.csv'
'''
Y_S = 10
Y_E = 100 #50



def InitPop(N, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    pop_list = list()
    import random

    while len(pop_list) < N:
        #x=[1,1,2,...,10]
        xi = random.randint(x_s, x_e)
        #y=[1,2,...,100]
        yi = random.randint(y_s, y_e)

        xibit = initpop.Dec2bit(xi, bitCount_x)
        yibit = initpop.Dec2bit(yi, bitCount_y)
        oneStr = xibit + yibit
        pop_list.append(oneStr)
        #print xi, xibit, yi, yibit, oneStr
    return  pop_list


def Write2CSV(listlist, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)
    print fileName

if __name__ == '__main__':
    allFileName =  sys.argv[1]

    fitness.loadFitness(FITNESSFILENAME) #set OBJECT_STRUCT_DICT
    OBJECT_STRUCT_DICT = config.get_object_struct()
    for serv in OBJECT_STRUCT_DICT:
        for thr_int in OBJECT_STRUCT_DICT[serv]:
            one = OBJECT_STRUCT_DICT[serv][thr_int]
            #print serv, thr_int, one.nonlapClassCount, one.nonlapClassCount_avg, one.withinWorkflow, one.interWorklow, one.APINum, one.APINum_avg
    #print 'loadFitness finished....\n'

    all_result_list = list()
    all_result_list.append(['servnum', 'thr', 'overlapClassCount', 'interWorklow', 'interCallNum', 'APINum', 'withinWorkflow', 'repeatClassCount', 'realClusterNum'])

    pop_list = InitPop(30, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
    for indiv in pop_list:
        [xi, yi] = initpop.TransCode2Indiv(indiv, BIT_COUNT_X, BIT_COUNT_Y)
        one = OBJECT_STRUCT_DICT[xi][yi]
        all_result_list.append([xi, yi, one.overlapClassCount, one.interWorklow, one.interCallNum, one.APINum, one.withinWorkflow, -one.repeatClassCount, one.realClusterNum])

    #save to csv
    Write2CSV(all_result_list, allFileName)
