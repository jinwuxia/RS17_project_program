#quicky non dominate sort for polulation


def IsEqualandBig(value1, value2):
    if value1 >= value2:
        return True
    else:
        return False

def IsBig(value1, value2):
    if value1 > value2:
        return True
    else:
        return False


#if indi_2 all better(strongly), return True.  indiv1 is dominated by indiv2
def IsDominated(indiv_1, indiv_2):
    import fitness
    import config
    fitness_method_list = config.GlobalVar.FITNESS_METHOD_LIST
    counter_equalbig = 0
    counter_big = 0
    for fitness_method in fitness_method_list:
        if IsEqualandBig(fitness.GetFitness(fitness_method, indiv_2), fitness.GetFitness(fitness_method, indiv_1)):
            counter_equalbig += 1
        if IsBig(fitness.GetFitness(fitness_method, indiv_2), fitness.GetFitness(fitness_method, indiv_1)):
            counter_big += 1

    if counter_equalbig == len(fitness_method_list) and counter_big > 0:
        return True
    else:
        return False



#if indiv_1 dominate(all better than ) indiv_2, return True
def Dominate(indiv_1, indiv_2):
    import fitness
    import config
    fitness_method_list = config.GlobalVar.FITNESS_METHOD_LIST
    counter_big = 0
    counter_equalbig = 0
    for fitness_method in fitness_method_list:
        if IsEqualandBig(fitness.GetFitness(fitness_method, indiv_1), fitness.GetFitness(fitness_method, indiv_2)):
            counter_equalbig += 1
        if IsBig(fitness.GetFitness(fitness_method, indiv_1), fitness.GetFitness(fitness_method, indiv_2)):
            counter_big += 1

    if counter_equalbig == len(fitness_method_list) and counter_big > 0:
        return True
    else:
        return False


#for each indiv, compute the worseSet which is dominated by it. dominatedDict[indiv] = set
#compute  the better indiv number which dominate it.  isDominatedDict[indiv] = count
#return dominateSetDict[indiv1]=set(indiv,....)
#       isDominatedDict[indiv] = count
def InitDominate(pop_list):
    dominateSetDict = dict()
    isDominatedDict = dict()
    for indiv in pop_list:
        dominateSetDict[indiv] = set()
        isDominatedDict[indiv] = 0
    for i in range(0, len(pop_list)):
        indiv_i = pop_list[i]
        for j in range(0, len(pop_list)):
            if i != j:
                indiv_j = pop_list[j]
                if IsDominated(indiv_i, indiv_j):
                    if indiv_i not in isDominatedDict:
                        isDominatedDict[indiv_i] = 1
                    else:
                        isDominatedDict[indiv_i] += 1
                if Dominate(indiv_i, indiv_j):
                    if indiv_i not in dominateSetDict:
                        dominateSetDict[indiv_i] = set()
                    dominateSetDict[indiv_i].add(indiv_j)
    return dominateSetDict, isDominatedDict

#return layerList , and indiv's rank/layer number
def FastNondomSort(pop_list):
    [dominateSetDict, isDominatedDict] = InitDominate(pop_list)
    #print 'dominateSetDict=', dominateSetDict
    #print 'isDominatedDict=', isDominatedDict
    layerList = list() #list[1] = [indiv1. ....]
    indivRankDict = dict() #[indiv] = rank
    #init F_list
    F_list = list()
    for indiv in pop_list:
        if isDominatedDict[indiv] == 0:
            F_list.append(indiv)

    layer = 0
    while len(F_list) != 0:
        new_F_list = list()
        for indiv_i in F_list:
            oneset = dominateSetDict[indiv_i]
            for indiv_j in oneset:
                isDominatedDict[indiv_j] -= 1
                if isDominatedDict[indiv_j] == 0:
                    new_F_list.append(indiv_j)
        #current layer save, and use a new layer
        layerList.append(F_list)
        F_list = new_F_list
        #print 'layer: ', layer, '=', layerList[layer]
        layer += 1
    #print 'quick nondoninate sort end..........\n'

    for rank in range(0, len(layerList)):
        for indiv in layerList[rank]:
            indivRankDict[indiv] = rank

    return layerList, indivRankDict

#return the indiv's rank/layer
def GetIndivRank(indiv, indivRankDict):
    return indivRankDict[indiv]
