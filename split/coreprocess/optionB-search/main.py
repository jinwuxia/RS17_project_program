#judge the search iteration condition
def IsStop():
    return True

def MainFunc():
    #step1: init population
    N = 6 #initial populization size
    x_s = 1
    x_e = 10
    y_s = 1
    y_e = 100

    selected_method = 'PRO'  #PRO or SA
    tem = 100
    cooling_rate = 0.98

    cross_operator = ''


    pop_list = InitPop(N, x_s, x_e, y_s, y_e)

    old_pop_list = list()
    old_fitness_value_list = list()
    while(True):
        #step2: compute finess
        fitness_value_list = list()
        for index  in range(0, len(pop_list)):
            indiv = pop_list[index]
            fitness_value_list[index] = Fitness(indiv)

        #step3: select better ones as parents for reproduction
        if selected_method == 'PRO':
            selected_pop_list = SelectPop_Pro(pop_list, fitness_value_list)
        elif selected_method == 'SA':
            if len(old_pop_list) == 0:
                selected_pop_list = SelectPop_Pro(pop_list, fitness_value_list)
            else:
                selected_pop_list = SelectPop_SA(pop_list, fitness_value_list, old_pop_list, old_fitness_value_list, tem)
                tem = tem * cooling_rate
        else:
            print 'Unknown selecting method: ', selected_method

        #step4: crossover by using selected_pop, generate new generation
        new_pop_list = Crossover(selected_pop_list, cross_operator)

        #step5: muatition in a small probability
        new_pop_list = Mutation(new_pop_list)

        #record states
        old_pop_list = selected_pop_list  #old, parents
        pop_list = new_pop_list  #new, children
        old_fitness_value_list = fitness_value_list  #old

        if IsStop() == True:
            break
