import msmetric

#entry point: to get one fitness for each indiv
def getFitness(fitnessMethod, indiv):
    if fitnessMethod == "call coh without weight":
        return msmetric.get_call_coh_ForIndiv(indiv)

    if fitnessMethod == "call coup without weight":
        return -msmetric.get_call_coup_ForIndiv(indiv)

    if fitnessMethod == "concern coh without weight":
        return msmetric.get_con_coh_ForIndiv(indiv)

    if fitnessMethod == "concern coup without weight":
        return -msmetric.get_con_coup_ForIndiv(indiv)

    else:
        print("Do not support this fitness:", fitnessMethod)




#get fitness for a popoluation.
#population=[indiv, indiv, ...]
#fitness_method = onefitness
def getFitnessForPopulation(population, fitness_method):
    fitnessValue_list = list()
    for indiv in population:
        value = getFitness(fitness_method, indiv)
        fitnessValue_list.append(value)
    return fitnessValue_list
