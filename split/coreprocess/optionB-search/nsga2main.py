#if kegen == 1:#for geneation =1, use the jinbiaosai select the parents
def GenFirstGeneration():
    [parentA_list, parentB_list] = selectpop.SelectPop_Jinbiao(pop_list, fitness_value_list, N) #N pairs

    children_list = list()
    for index in range(0, N):
        [childA, childB] = crossover.Crossover_2P2C(parentA_list[index], parentB_list[index], BIT_COUNT_X, BIT_COUNT_Y)
        children_list.append(childA)
        children_list.append(childB)

    import random
    mutation_rd = random.random()
    if mutation_rd < MUTATION_PROBABILITY:
        print 'Mutation...'
        tmp_fitness_value_list = fitness.GetFitnessList(FITNESS_METHOD, children_list, BIT_COUNT_X, BIT_COUNT_Y)
        #make sure the mutation result is valid
        mutated_children_list = mutation.Mutation(children_list, tmp_fitness_value_list, MUTATION_OPERATOR,\
                                                 X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)

    pop_list.extend(parentA_list)
    pop_list.extend(parentB_list)
    pop_list.extend(mutated_children_list)
    return pop_list


def GenOtherGeneration():
    [layerList, indivRankDict] = FastNondomSort(pop_list)
    indivCrowdDict = ComputeCrowd(layerList, fitnessMethodList)
    parents_list = list()
    #sort first by rank, the by crowd
    #selected parents

    #crossover

    #mutation

    #merge parents and children

    return new_pop_list



def MainFunc():
    import config
    N = config.GlobalVar.N #initial populization size, each generation size = intialSize
    X_S = config.GlobalVar.X_S
    X_E = config.GlobalVar.X_E
    Y_S = config.GlobalVar.Y_S
    Y_E = config.GlobalVar.Y_E
    BIT_COUNT_X = config.GlobalVar.BIT_COUNT_X
    BIT_COUNT_Y = config.GlobalVar.BIT_COUNT_Y
    FITNESSFILENAME = config.GlobalVar.FITNESSFILENAME
    CROSS_OPERATOR = config.GlobalVar.CROSS_OPERATOR
    MUTATION_PROBABILITY = config.GlobalVar.MUTATION_PROBABILITY
    MUTATION_OPERATOR = config.GlobalVar.MUTATION_OPERATOR

    import initpop
    import selectpop
    import fitness
    import crossover
    import mutation
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
            pop_list = GenFirstGeneration()
        else:
            pop_list = GenOtherGeneration()
