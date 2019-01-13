import random


#when "random mutation", random choose a indiv, random choose a np .
def mutation_process(pop_list, mutation_operator):
    mutation_indiv_index = -1
    if mutation_operator == 'random': #randomly choose one indiv to mutate
        mutation_indiv_index = random.randint(0, len(pop_list) - 1)
    #elif mutation_operator == 'worse': #choose the worse one indiv to mutate
    #    mutation_indiv_index = fitness_value_list.index( min(fitness_value_list) )
    else:
        print ('Unknown mutation operator: ', mutation_operator)

    new_indiv  = mutationOnIndiv(pop_list[mutation_indiv_index] )
    pop_list[mutation_indiv_index] = new_indiv
    return pop_list


# random choose a children from this parent's children
def mutationOnIndiv(indiv):
    import mscrossover
    children = mscrossover.crossover_1PNC(indiv)
    index = random.randint(0, len(children) - 1)
    #print(indiv, " mutate into ",  children[index])
    return children[index]


def mutation(pop_list, mutation_operator, mutation_probabilty):
    mutation_rd = random.random()
    if mutation_rd < mutation_probabilty:
        #print("mutation happens ", mutation_rd, mutation_probabilty)
        return mutation_process(pop_list, mutation_operator)
    else:
        #print("no mutation ", mutation_rd, mutation_probabilty)
        return pop_list
