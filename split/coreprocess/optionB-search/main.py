OBJECT_STRUCT_DICT = dict()

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
def IsStop(kgen, old_pop_list, new_pop_list, old_fitness_value_list, new_fitness_value_list):
    print 'old_pop_list=           ', old_pop_list
    print 'new_pop_list=           ', new_pop_list
    print 'old_fitness_value_list= ', old_fitness_value_list
    print 'new_fitness_value_list= ', new_fitness_value_list
    if kgen > 10000:
        return True
    if len(new_pop_list) == 1:
        return True

    old_avg = sum(old_fitness_value_list) / len(old_fitness_value_list)
    new_avg = sum(new_fitness_value_list) / len(new_fitness_value_list)
    print 'old fitness avg=        ', old_avg
    print 'new fitness avg=        ', new_avg
    
    if kgen > 5000 and abs(old_avg - new_avg) <= 0.00001:
        return True
    return False

def CheckChildrenValid(new_pop_list, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    import initpop
    invalidLen = 0
    for indiv in new_pop_list:
        if initpop.IsValidIndiv(indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y) == False:
            invalidLen += 1
    return invalidLen


def GetFitnessList(pop_list, BIT_COUNT_X,  BIT_COUNT_Y):
    global OBJECT_STRUCT_DICT
    import initpop
    fitness_value_list = list()
    for index  in range(0, len(pop_list)):
        indiv = pop_list[index]
        [x, y] = initpop.TransCode2Indiv(indiv, BIT_COUNT_X, BIT_COUNT_Y)  #=[x,y]=[serv, thr_int]
        fitness_value_list.append(OBJECT_STRUCT_DICT[x][y].withinWorkflow)
    return fitness_value_list

def MainFunc():
    global OBJECT_STRUCT_DICT
    OBJECT_STRUCT_DICT = dict()

    #step1: init population
    N = 6 #initial populization size, each generation size = intialSize
    X_S = 2
    X_E = 10
    Y_S = 1
    Y_E = 100
    BIT_COUNT_X = 4
    BIT_COUNT_Y = 7

    FITNESSFILENAME = '../../../testcase_data/jpetstore6/coreprocess/jpetstore6-fitness.csv'

    SELECTED_METHOD = 'SA'  #PRO or SA
    FITNESS_PROBABILITY = 0.10
    TEM = 100
    COOLING_RATE = 0.98

    CROSS_OPERATOR = '2P2C'
    #CHILDREN_NUM = 4

    MUTATION_PROBABILITY = 0.02
    MUTATION_OPERATOR = 'random' #random  or worse

    import fitness
    OBJECT_STRUCT_DICT = fitness.loadFitness(FITNESSFILENAME)
    for serv in OBJECT_STRUCT_DICT:
        for thr_int in OBJECT_STRUCT_DICT[serv]:
            one = OBJECT_STRUCT_DICT[serv][thr_int]
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
        fitness_value_list = GetFitnessList(pop_list, BIT_COUNT_X, BIT_COUNT_Y)
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
            invalidLen = CheckChildrenValid(new_pop_list, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
            if invalidLen == 0:
                print 'After crossover, new_pop_list=', new_pop_list
                break
            else:
                print 'invalidLen = ', invalidLen, ';    continue crossover...'


        #step5: mutation in a small probability
        import mutation
        import random
        mutation_rd = random.random()
        if mutation_rd < MUTATION_PROBABILITY:
            print 'Mutation...'
            tmp_fitness_value_list = GetFitnessList(pop_list, BIT_COUNT_X, BIT_COUNT_Y)
            #make sure the mutation result is valid
            new_pop_list = mutation.Mutation(new_pop_list, tmp_fitness_value_list, MUTATION_OPERATOR,\
                                             X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)
            print 'after Mutation, new_pop_list: ', new_pop_list

        #old_pop_list  and selected_pop_list are both the parents.
        if IsStop(kgen, old_pop_list, selected_pop_list, old_fitness_value_list, fitness_value_list):
            break
        #record states
        old_pop_list = selected_pop_list  #old, parents
        pop_list = new_pop_list  #new, children
        old_fitness_value_list = fitness_value_list  #old
        kgen += 1

MainFunc()
