#quicky non dominate sort for polulation

#if indi_2 all better, return True.  indiv1 is dominated by indiv2
def IsDominated(indiv_1, indiv_2):
    if fitness1(indiv_2) >= fitness1(indiv_1) and fitness2(indiv_2) >= fitness2(indiv_1):
        return True
    else:
        return False

#if indiv_1 dominate(all better than ) indiv_2, return True
def Dominate(indiv_1, indiv_2):
    if fitness1(indiv_1) >= fitness1(indiv_2) and fitness2(indiv_1) >= fitness2(indiv_2):
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
                        dominateSetDict[indiv_1] = set()
                    dominateSetDict[indiv_1].add(indiv_j)
    return dominateSetDict, isDominatedDict

#return layerList , and indiv's rank/layer number
def QuickNondomSort(pop_list):
    [dominateSetDict, isDominatedDict] = InitDominate(pop_list)
    layerList = list() #list[1] = [indiv1. ....]
    indivRankDict = dict() #[indiv] = rank
    #init F_list
    F_list = list()
    for indiv in pop_list:
        if isDominatedDict[indiv] == 0:
            F_list.append(indiv)

    layer = 0
    while len(F_list) != 0:
        for indiv_i in F_list:
            oneset = dominateSetDict[indiv_i]
            for indiv_j in oneset:
                isDominatedDict[indiv_j] -= 1
                if isDominatedDict[indiv_j] == 0:
                    new_F_list.append(indiv_j)
        #current layer save, and use a new layer
        layerList.append(F_list)
        F_list = new_F_list
        print 'layer: ', layer, '=', layerList[layer]
        layer += 1
    print 'qcuick nondoninate sort end..........'

    for rank in range(0, len(layerList)):
        for indiv in layerList[rank]:
            indivRankDict[indiv] = rank

    return layerList, indivRankDict

#return the indiv's rank/layer
def GetIndivRank(indiv, indivRankDict):
    return indivRankDict[indiv]
