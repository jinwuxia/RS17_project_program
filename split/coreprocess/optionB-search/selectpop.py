
#selected better parents by using Probility of fitness_function_value
#pop_list and fitness_value_list are corresponding
def SelectPop_Pro(pop_list, fitness_value_list, probability):
    selected_pop_list = list()

    fenmu = sum(fitness_value_list)
    pro_list = [each / float(fenmu) for each in fitness_value_list]
    print 'probability: ', pro_list
    for index in range(0, len(pop_list)):
        if pro_list[index] >= probability:
            selected_pop_list.append(pop_list[index])

    if len(selected_pop_list) % 2 == 1:  #if is even, repeate one randomly, generate one for the last element
        import random
        rindex = random.randint(0, len(selected_pop_list) - 2)
        selected_pop_list.append(selected_pop_list[rindex])

    #print 'selected_pop_list:', selected_pop_list
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
        if e_new >= e_old:   #p=1 accepted
            selected_pop_list.append(new_pop_list[index])
        else:
            detE = (e_new - e_old)
            accept_bad_pro = min(1, math.exp(detE/float(t)))
            print 'detE=', detE, 'math.exp(detE/float(t))=', math.exp(detE/float(t)), 'accepted_bad_pro=', accept_bad_pro
            p = random.random()
            if p <= accept_bad_pro:  #accept
                print 'SA accpted bad, p=', p
                selected_pop_list.append(new_pop_list[index])
            else:
                selected_pop_list.append(old_pop_list[index])

    return selected_pop_list
