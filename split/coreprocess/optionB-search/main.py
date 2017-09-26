



class ObjectStruct:
    def __init__(self, nonlapClassCount, nonlapClassCount_avg, overlapClassCount, overlapClassCount_avg, \
                    realClusterNum, repeatClassCount, repeatClassCount_avg,\
                    interWorklow, withinWorkflow, interCallNum, interCallNum_avg, \
                    interCallNum_f, interCallNum_avg_f, APINum, APINum_avg):
        self.nonlapClassCount = nonlapClassCount
        self.nonlapClassCount_avg = nonlapClassCount_avg
        self.overlapClassCount = overlapClassCount
        self.overlapClassCount_avg = overlapClassCount_avg
        self.realClusterNum = realClusterNum
        self.repeatClassCount = repeatClassCount
        self.repeatClassCount_avg  =repeatClassCount_avg
        self.interWorklow = interWorklow
        self.withinWorkflow = withinWorkflow
        self.interCallNum = interCallNum
        self.interCallNum_avg = interCallNum_avg
        self.interCallNum_f = interCallNum_f
        self.interCallNum_avg_f = interCallNum_avg_f
        self.APINum = APINum
        self.APINum_avg = APINum_avg


#judge the search iteration condition
def IsStop():
    return False


def checkChildrenValid(new_pop_list, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    import initpop
    invalidLen = 0
    for indiv in new_pop_list:
        if initpop.IsValidIndiv(indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y) == False:
            invalidLen += 1
    return invalidLen

def MainFunc():
    #step1: init population
    N = 6 #initial populization size, each generation size = intialSize
    X_S = 2
    X_E = 10
    Y_S = 1
    Y_E = 100
    BIT_COUNT_X = 4
    BIT_COUNT_Y = 7

    FITNESSFILENAME = '../../../testcase_data/jpetstore6/coreprocess/jpetstore6-fitness.csv'

    SELECTED_METHOD = 'PRO'  #PRO or SA
    FITNESS_PROBABILITY = 0.10
    TEM = 100
    COOLING_RATE = 0.98

    CROSS_OPERATOR = '2P2C'
    CHILDREN_NUM = 4

    MUTATION_PROBABILITY = 0.02
    import fitness
    objectStructDict = fitness.loadFitness(FITNESSFILENAME)
    for serv in objectStructDict:
        for thr_int in objectStructDict[serv]:
            one = objectStructDict[serv][thr_int]
            print serv, thr_int, one.nonlapClassCount, one.nonlapClassCount_avg, one.withinWorkflow, one.interWorklow, one.APINum, one.APINum_avg
    print 'loadFitness finished....\n'

    #step 1
    import initpop
    pop_list = initpop.InitPop(N, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
    print 'init pop: ', pop_list
    print 'population initialization finished....\n'

    old_pop_list = list()
    old_fitness_value_list = list()
    kgen = 1
    while(True):
        print 'loop: ', kgen
        #step2: compute finess
        fitness_value_list = list()
        for index  in range(0, len(pop_list)):
            indiv = pop_list[index]
            [x, y] = initpop.TransCode2Indiv(indiv, BIT_COUNT_X, BIT_COUNT_Y)  #=[x,y]=[serv, thr_int]
            fitness_value_list.append(objectStructDict[x][y].withinWorkflow)
            #print fitness_value_list[index]
        print 'fitness_value: ', fitness_value_list

        #step3: select better ones as parents for reproduction
        import selectpop
        if SELECTED_METHOD == 'PRO':
            selected_pop_list = selectpop.SelectPop_Pro(pop_list, fitness_value_list, FITNESS_PROBABILITY)
        elif SELECTED_METHOD == 'SA':
            if len(old_pop_list) == 0:
                selected_pop_list = selectpop.SelectPop_Pro(pop_list, fitness_value_list, FITNESS_PROBABILITY)
            else:
                selected_pop_list = selectpop.SelectPop_SA(pop_list, fitness_value_list, old_pop_list, old_fitness_value_list, TEM)
                TEM = TEM * COOLING_RATE
        else:
            print 'Unknown selecting method: ', SELECTED_METHOD
        print 'selected pop: ', selected_pop_list
        print 'selected population end.....'

        #step4: crossover by using selected_pop, generate new generation
        import crossover
        print 'Crossover.....'
        while True:
            new_pop_list = crossover.Crossover([BIT_COUNT_X, BIT_COUNT_Y], selected_pop_list, CROSS_OPERATOR)
            invalidLen = checkChildrenValid(new_pop_list, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
            if invalidLen == 0:
                print 'After crossover, new_pop_list=', new_pop_list
                break
            else:
                print 'invalidLen = ', invalidLen, ';    continue crossover...'

        '''
        #step5: muatition in a small probability
        import mutation
        import random
        mutation_rd = random.random()
        if mutation_rd < MUTATION_PROBABILITY:
            print 'Mutation...'
            new_pop_list = mutation.Mutation(new_pop_list)
            print 'after Mutation, new_pop_list: ', new_pop_list
        '''

        #record states
        old_pop_list = selected_pop_list  #old, parents
        pop_list = new_pop_list  #new, children
        old_fitness_value_list = fitness_value_list  #old

        if IsStop() == True:
            break
        kgen += 1

MainFunc()
