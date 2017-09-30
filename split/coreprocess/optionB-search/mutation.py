
def MutationOnIndiv(indiv):
    import random
    index = random.randint(0, len(indiv) - 1)
    if indiv[index] == '0':
        substr = '1'
    else:
        substr = '0'
    mu_indiv = indiv[0:index] + substr + indiv[index + 1: len(indiv)]
    print 'mutation index=', index, ' indiv=', indiv, '  mu_indiv=', mu_indiv
    return mu_indiv


#if mutation = random, then fitness_value_list no use
def Mutation(pop_list, fitness_value_list, mutation_operator, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
    mutation_indiv_index = -1
    if mutation_operator == 'random': #randomly choose one indiv to mutate
        import random
        mutation_indiv_index = random.randint(0, len(pop_list) - 1)
    elif mutation_operator == 'worse': #choose the worse one indiv to mutate
        mutation_indiv_index = fitness_value_list.index( min(fitness_value_list) )
    else:
        print 'Unknown mutation operator: ', mutation_operator

    new_indiv  = MutationOnIndiv( pop_list[mutation_indiv_index] )
    import initpop
    if initpop.IsValidIndiv(new_indiv, x_s, x_e, y_s, y_e, bitCount_x, bitCount_y):
        pop_list[mutation_indiv_index] = new_indiv
    return pop_list
