
#selected better parents by using Probility of fitness_function_value
#pop_list and fitness_value_list are corresponding
def SelectPop_Pro(pop_list, fitness_value_list, probability):
    selected_pop_list = list()

    fenmu = sum(fitness_value_list)
    pro_list = [each / float(fenmu) for each in fitness_value_list]
    for index in len(0, len(pop_list)):
        if pro_list[index] >= probability:
            selected_pop_list.append(pop_list[index])

    if len(selected_pop_list) / 2 == 1:  #if is even, repeate one randomly
        import random
        rindex = random.randint(0, len(selected_pop_list) - 1)
        selected_pop_list.append(selected_pop_list[rindex])
    return selected_pop_list

#selected better parents by using simulated annealing
#pop_list and fitness_value_list are corresponding
def SelectPop_SA(new_pop_list, new_fitness_value_list, old_pop_list, old_fitness_value_list, t):
    #Old and new are same size
    import math
    import random
    selected_pop_list = list()
    for index in range(0, len(new_pop_list)):
        e_new = new_fitness_value_list[index]
        e_old = old_fitness_value_list[index]
        if e_new < e_old:   #p=1 accepted
            selected_pop_list.append(new_pop_list[index])
        else:
            detE = -(e_new - e_old)
            accept_bad_pro = min(1, math.exp(detE/float(t)))
            p = random(0, 1)
            if p <= accept_bad_pro:  #accept
                selected_pop_list.append(new_pop_list[index])
            else:
                selected_pop_list.append(old_pop_list[index])

    return selected_pop_list
