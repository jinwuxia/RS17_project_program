'''
multi-object optimzation using NSGAII
'''
import sys
import csv
import config
import fitness
import fastnondomsort
import crowdfactorcal
import mutation
import selectpop
import crossover
import initpop
import random

N = config.GlobalVar.N #initial populization size, each generation size = intialSize
M = config.GlobalVar.M
K = config.GlobalVar.K
X_S = config.GlobalVar.X_S
X_E = config.GlobalVar.X_E
Y_S = config.GlobalVar.Y_S
Y_E = config.GlobalVar.Y_E
BIT_COUNT_X = config.GlobalVar.BIT_COUNT_X
BIT_COUNT_Y = config.GlobalVar.BIT_COUNT_Y
CROSS_OPERATOR = config.GlobalVar.CROSS_OPERATOR
MUTATION_PROBABILITY = config.GlobalVar.MUTATION_PROBABILITY
MUTATION_OPERATOR = config.GlobalVar.MUTATION_OPERATOR
FITNESSFILENAME = config.GlobalVar.FITNESSFILENAME
FITNESS_METHOD_LIST = config.GlobalVar.FITNESS_METHOD_LIST

class IndivObject:
    def __init__(self, indiv, rank, fucrowd):
        self.indiv = indiv
        self.rank = rank
        self.fucrowd = fucrowd

def CheckChildrenValid(new_pop_list, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    invalidLen = 0
    for indiv in new_pop_list:
        if initpop.IsValidIndiv(indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y) == False:
            invalidLen += 1
    return invalidLen


#if kegen == 1:#for geneation =1, use the jinbiaosai select the parents
def GenFirstGeneration(pop_list):
    [layerList, indivRankDict] = fastnondomsort.FastNondomSort(pop_list)
    [parentA_list, parentB_list] = selectpop.SelectPop_Jinbiao(layerList, M, K) #K pairs
    #print 'parentA:', parentA_list
    #print 'parentB:', parentB_list

    while True:
        children_list = list()
        for index in range(0, K):
            [childA, childB] = crossover.Crossover_2P2C(parentA_list[index], parentB_list[index], BIT_COUNT_X, BIT_COUNT_Y)
            children_list.append(childA)
            children_list.append(childB)
        children_list = list(set(children_list))
        invalidLen = CheckChildrenValid(children_list, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
        if invalidLen == 0:
            #print 'After crossover, new_pop_list=', children_list
            break
        else:
            #print 'invalidLen = ', invalidLen, ';    continue crossover...'
            print ''


    mutation_rd = random.random()
    if mutation_rd < MUTATION_PROBABILITY:
        #print 'Mutation...'
        #make sure the mutation result is valid
        children_list = mutation.Mutation(children_list, list(), 'random', X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
    pop_list.extend(parentA_list)
    pop_list.extend(parentB_list)
    pop_list.extend(children_list)
    return list(set(pop_list))

#selectedSize is the parens number
def GenOtherGeneration(pop_list, selectedSize):
    [layerList, indivRankDict] = fastnondomsort.FastNondomSort(pop_list)
    indivCrowdDict = crowdfactorcal.ComputeCrowd(layerList, FITNESS_METHOD_LIST)

    #sort first by rank, the by crowd
    pop_object_list = list()
    for indiv in pop_list:
        rank = indivRankDict[indiv]
        crowd = indivCrowdDict[indiv]
        pop_object_list.append(IndivObject(indiv, rank, -crowd)) #choose both min
    import operator
    cmpfunc = operator.attrgetter('rank', 'fucrowd')
    pop_object_list.sort(key = cmpfunc,  reverse = False)

    #step3: selected parents
    parents_list = list()
    for index in range(0, selectedSize):
        parents_list.append(pop_object_list[index].indiv)
    #print 'elicit selected over: ', parents_list

    #step4: crossover by using selected_pop, generate new generation
    #print 'Crossover.until all children are valid....'
    while True:
        children_list = crossover.Crossover([BIT_COUNT_X, BIT_COUNT_Y], parents_list, CROSS_OPERATOR)
        invalidLen = CheckChildrenValid(children_list, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
        if invalidLen == 0:
            #print 'After crossover, children_list=', children_list
            break
        else:
            print ''
            #print 'invalidLen = ', invalidLen, ';    continue crossover...'


    #step5: mutation in a small probability
    mutation_rd = random.random()
    if mutation_rd < MUTATION_PROBABILITY:
        #print 'Mutation...'
        #make sure the mutation result is valid
        children_list = mutation.Mutation(children_list, list(), MUTATION_OPERATOR,\
                                             X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
        #print 'after Mutation, children_list: ', children_list


    #merge parents and children
    merged_pop_list = list()
    merged_pop_list.extend(parents_list)
    merged_pop_list.extend(children_list)
    return merged_pop_list


#judge the search iteration condition
def IsStop(kgen, old_pop_list, new_pop_list):
    import config
    import initpop
    old_pop_num_list = list()
    for each in old_pop_list:
        [x, y] = initpop.TransCode2Indiv(each, BIT_COUNT_X, BIT_COUNT_Y)
        old_pop_num_list.append(str(x) + ',' + str(y))
    new_pop_num_list = list()
    for each in new_pop_list:
        [x, y] = initpop.TransCode2Indiv(each, BIT_COUNT_X, BIT_COUNT_Y)
        new_pop_num_list.append(str(x) + ',' + str(y))
    #print 'old_pop_list=           ', old_pop_list, '; ', old_pop_num_list
    #print 'new_pop_list=           ', new_pop_list, '; ', new_pop_num_list

    if kgen > config.GlobalVar.MAX_ITERATION_LOOP:
        return True
    if len(new_pop_list) == 1:
        return True
    old_fitness_value_list1 = fitness.GetFitnessList('withinwf', old_pop_list)
    old_fitness_value_list2 = fitness.GetFitnessList('clusternum', old_pop_list)
    old_fitness_value_list3 = fitness.GetFitnessList('repclassnum', old_pop_list)
    new_fitness_value_list1 = fitness.GetFitnessList('withinwf', new_pop_list)
    new_fitness_value_list2 = fitness.GetFitnessList('clusternum', new_pop_list)
    new_fitness_value_list3 = fitness.GetFitnessList('repclassnum', new_pop_list)
    old_avg1 = sum(old_fitness_value_list1) / len(old_fitness_value_list1)
    new_avg1 = sum(new_fitness_value_list1) / len(new_fitness_value_list1)
    old_avg2 = sum(old_fitness_value_list2) / len(old_fitness_value_list2)
    new_avg2 = sum(new_fitness_value_list2) / len(new_fitness_value_list2)
    old_avg3 = sum(old_fitness_value_list3) / len(old_fitness_value_list3)
    new_avg3 = sum(new_fitness_value_list3) / len(new_fitness_value_list3)

    #print 'old fitness avg=  withinwf, clusternum, repclassnum = ', old_avg1, old_avg2, old_avg3
    #print 'new fitness avg=  withinwf, clusternum, repclassnum = ', new_avg1, new_avg2, new_avg3

    #is stable
    if abs(old_avg1 - new_avg1) <= 0.00001 and abs(old_avg2 - new_avg2) <= 0.00001 and abs(old_avg3 - new_avg3) <= 0.00001:  #on line
        config.add_continue_best_loop()  #crrrent + 1
    else:
        config.reset_continue_best_loop()#reset current = 0
    if config.get_continue_best_loop() > config.GlobalVar.CONTINUE_BEST_LOOP:
        return True

    return False

def Mainloop():
    #step 1
    pop_list = initpop.InitPop(N, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
    print 'init pop: ', pop_list
    print 'population initialization finished....\n'

    kgen = 1
    while(True):
        if kgen == 1:
            new_pop_list = GenFirstGeneration(pop_list)
            print 'generate 1 st = ', new_pop_list, '\n'
        else:
            new_pop_list = GenOtherGeneration(pop_list, selectedSize=config.GlobalVar.K)
            print 'generate', kgen, 'st =', new_pop_list, '\n'
        if IsStop(kgen, pop_list, new_pop_list):
            break
        else:
            pop_list = new_pop_list
            kgen += 1

    return new_pop_list


def Write2CSV(listlist, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)
    print fileName

if __name__ == '__main__':
    allFitnessFileName = sys.argv[1]
    bestFitnessFileName = sys.argv[2]

    fitness.loadFitness(FITNESSFILENAME) #set OBJECT_STRUCT_DICT
    OBJECT_STRUCT_DICT = config.get_object_struct()
    for serv in OBJECT_STRUCT_DICT:
        for thr_int in OBJECT_STRUCT_DICT[serv]:
            one = OBJECT_STRUCT_DICT[serv][thr_int]
            print serv, thr_int, one.nonlapClassCount, one.nonlapClassCount_avg, one.withinWorkflow, one.interWorklow, one.APINum, one.APINum_avg
    print 'loadFitness finished....\n'

    best_fitness_list = list()
    best_fitness_list.append(['withinWorkflow', '-repeatClassCount', 'realClusterNum'])
    all_fitness_list = list()
    all_fitness_list.append(['servnum', 'thr', 'overlapClassCount', 'interWorklow', 'interCallNum', 'APINum', 'withinWorkflow', '-repeatClassCount', 'realClusterNum'])
    for times in range(0, 30):
        new_pop_list = Mainloop()
        for indiv in new_pop_list:
            [xi, yi] = initpop.TransCode2Indiv(indiv, BIT_COUNT_X, BIT_COUNT_Y)
            one = OBJECT_STRUCT_DICT[xi][yi]
            all_fitness_list.append([xi, yi, one.overlapClassCount, one.interWorklow,\
                one.interCallNum, one.APINum, one.withinWorkflow, -one.repeatClassCount, one.realClusterNum])

        withinWorkflow_tmp = list()
        repeatClassCount_tmp = list()
        realClusterNum_tmp = list()
        for indiv in new_pop_list:
            [xi, yi] = initpop.TransCode2Indiv(indiv, BIT_COUNT_X, BIT_COUNT_Y)
            one = OBJECT_STRUCT_DICT[xi][yi]
            withinWorkflow_tmp.append(one.withinWorkflow)
            repeatClassCount_tmp.append(-one.repeatClassCount)
            realClusterNum_tmp.append(one.realClusterNum)
        withinWorkflow_best = max(withinWorkflow_tmp)
        repeatClassCount_best = max(repeatClassCount_tmp)
        realClusterNum_best = max(realClusterNum_tmp)
        best_fitness_list.append([withinWorkflow_best, repeatClassCount_best, realClusterNum_best])

    Write2CSV(all_fitness_list, allFitnessFileName)
    Write2CSV(best_fitness_list ,bestFitnessFileName)
