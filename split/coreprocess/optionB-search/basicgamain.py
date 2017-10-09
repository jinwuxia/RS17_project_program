'''
single pbject optimzation
'''


#judge the search iteration condition
def IsStop(kgen, old_pop_list, new_pop_list, old_fitness_value_list, new_fitness_value_list):
    import config
    import initpop
    old_pop_num_list = list()
    for each in old_pop_list:
        [x, y] = initpop.TransCode2Indiv(each, config.GlobalVar.BIT_COUNT_X,  config.GlobalVar.BIT_COUNT_Y)
        old_pop_num_list.append(str(x) + ',' + str(y))
    new_pop_num_list = list()
    for each in new_pop_list:
        [x, y] = initpop.TransCode2Indiv(each, config.GlobalVar.BIT_COUNT_X,  config.GlobalVar.BIT_COUNT_Y)
        new_pop_num_list.append(str(x) + ',' + str(y))
    print 'old_pop_list=           ', old_pop_list, '; ', old_pop_num_list
    print 'new_pop_list=           ', new_pop_list, '; ', new_pop_num_list
    print 'old_fitness_value_list= ', old_fitness_value_list
    print 'new_fitness_value_list= ', new_fitness_value_list

    if kgen > config.GlobalVar.MAX_ITERATION_LOOP:
        return True
    if len(new_pop_list) == 1:
        return True
    if len(old_pop_list) == 0:
        return False
    old_avg = sum(old_fitness_value_list) / len(old_fitness_value_list)
    new_avg = sum(new_fitness_value_list) / len(new_fitness_value_list)
    print 'old fitness avg=        ', old_avg
    print 'new fitness avg=        ', new_avg
    print 'old max_fitness avg=        ', max(old_fitness_value_list)
    print 'new max_fitness avg=        ', max(new_fitness_value_list)

    #is stable
    if abs(old_avg - new_avg) <= 0.00001:  #on line
        config.add_continue_best_loop()  #crrrent + 1
    else:
        config.reset_continue_best_loop()#reset current = 0
    if config.get_continue_best_loop() > config.GlobalVar.CONTINUE_BEST_LOOP:
        return True

    return False

def CheckChildrenValid(new_pop_list, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    import initpop
    invalidLen = 0
    for indiv in new_pop_list:
        if initpop.IsValidIndiv(indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y) == False:
            invalidLen += 1
    return invalidLen



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
    SELECTED_METHOD = config.GlobalVar.SELECTED_METHOD
    FITNESS_PROBABILITY = config.GlobalVar.FITNESS_PROBABILITY
    FITNESS_METHOD = config.GlobalVar.FITNESS_METHOD
    TEM = config.GlobalVar.TEM
    COOLING_RATE = config.GlobalVar.COOLING_RATE
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

    old_pop_list = list()
    old_fitness_value_list = list()
    kgen = 1
    while(True):
        print 'loop: ', kgen
        #step2: compute finess
        fitness_value_list = fitness.GetFitnessList(FITNESS_METHOD, pop_list)
        print 'fitness_value: ', fitness_value_list

        #step3: select better ones as parents for reproduction
        if SELECTED_METHOD == 'PRO':
            selected_pop_list = selectpop.SelectPop_Pro(pop_list, fitness_value_list, FITNESS_PROBABILITY)
        elif SELECTED_METHOD == 'SA':
            if len(old_pop_list) == 0:
                selected_pop_list = selectpop.SelectPop_Pro(pop_list, fitness_value_list, FITNESS_PROBABILITY)
            else:
                print 'current temperature: ', TEM
                selected_pop_list = selectpop.SelectPop_SA(pop_list, fitness_value_list, old_pop_list, old_fitness_value_list, TEM)
                TEM = TEM * COOLING_RATE
        else:
            print 'Unknown selecting method: ', SELECTED_METHOD
        print 'selected pop: ', selected_pop_list
        print 'selected population end.....'

        #step4: crossover by using selected_pop, generate new generation
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
        import random
        mutation_rd = random.random()
        if mutation_rd < MUTATION_PROBABILITY:
            print 'Mutation...'
            tmp_fitness_value_list = fitness.GetFitnessList(FITNESS_METHOD, pop_list)
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
