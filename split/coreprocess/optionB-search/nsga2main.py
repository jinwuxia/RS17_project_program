import config
import fitness
import fastnondomsort
import crowdfactorcal
import mutation
import selectpop
import crossover
import initpop

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
    print 'parentA:', parentA_list
    print 'parentB:', parentB_list

    while True:
        children_list = list()
        for index in range(0, K):
            [childA, childB] = crossover.Crossover_2P2C(parentA_list[index], parentB_list[index], BIT_COUNT_X, BIT_COUNT_Y)
            children_list.append(childA)
            children_list.append(childB)
        children_list = list(set(children_list))
        invalidLen = CheckChildrenValid(children_list, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
        if invalidLen == 0:
            print 'After crossover, new_pop_list=', children_list
            break
        else:
            print 'invalidLen = ', invalidLen, ';    continue crossover...'


    import random
    mutation_rd = random.random()
    if mutation_rd < MUTATION_PROBABILITY:
        print 'Mutation...'
        #make sure the mutation result is valid
        children_list = mutation.Mutation(children_list, list(), 'random', X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
    pop_list.extend(parentA_list)
    pop_list.extend(parentB_list)
    pop_list.extend(children_list)
    return list(set(pop_list))

#selectedSize is the parens number
def GenOtherGeneration(pop_list, selectedSize):
    [layerList, indivRankDict] = FastNondomSort(pop_list)
    indivCrowdDict = ComputeCrowd(layerList, fitnessMethodList)

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
    print 'elicit selected over: ', parents_list

    #step4: crossover by using selected_pop, generate new generation
    print 'Crossover.until all children are valid....'
    while True:
        children_list = crossover.Crossover([BIT_COUNT_X, BIT_COUNT_Y], parents_list, CROSS_OPERATOR)
        invalidLen = CheckChildrenValid(children_list, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
        if invalidLen == 0:
            print 'After crossover, children_list=', children_list
            break
        else:
            print 'invalidLen = ', invalidLen, ';    continue crossover...'


    #step5: mutation in a small probability
    mutation_rd = random.random()
    if mutation_rd < MUTATION_PROBABILITY:
        print 'Mutation...'
        #make sure the mutation result is valid
        children_list = mutation.Mutation(children_list, list(), MUTATION_OPERATOR,\
                                             X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
        print 'after Mutation, children_list: ', children_list


    #merge parents and children
    merged_pop_list = lit()
    merged_pop_list.extend(parents_list)
    merged_pop_list.extend(children_list)
    return merged_pop_list



if __name__ == '__main__':
    fitness.loadFitness(FITNESSFILENAME) #set OBJECT_STRUCT_DICT
    OBJECT_STRUCT_DICT = config.get_object_struct()
    for serv in OBJECT_STRUCT_DICT:
        for thr_int in OBJECT_STRUCT_DICT[serv]:
            one = OBJECT_STRUCT_DICT[serv][thr_int]
            print serv, thr_int, one.nonlapClassCount, one.nonlapClassCount_avg, one.withinWorkflow, one.interWorklow, one.APINum, one.APINum_avg
    print 'loadFitness finished....\n'

    #step 1
    pop_list = initpop.InitPop(N, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
    print 'init pop: ', pop_list
    print 'population initialization finished....\n'


    kgen = 1
    while(True):
        if kgen == 1:
            #pop_list= ['01110101011', '01011001001', '10011010110', '10010101111']
            pop_list = GenFirstGeneration(pop_list)
            print 'generate 1 st = ', pop_list, '\n'
        else:
            pop_list = GenOtherGeneration(pop_list)
            print 'generate', kgen, 'st =', pop_list, '\n'
        if IsStop():
            break
        else:
            kgen += 1
