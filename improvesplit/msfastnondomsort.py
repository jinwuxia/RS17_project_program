#quicky non dominate sort for polulation
import msfitness
import msconfig



'''
for layerlist: each element is a tuple
for rankDict: each key is a tuple
'''
#alist = list of list
def myEncode(alist):
    tuples = list()
    for eachlist in alist:
        each = tuple(eachlist)
        tuples.append(each)
    res = tuple(tuples)
    #print(res)
    return res

def myDecode(atupe):
    reslist = list()
    for eachtupe in atupe:
        each = list(eachtupe)
        reslist.append(each)
    #print(atupe, " - ",  reslist)
    return reslist


def isEqualandBig(value1, value2):
    if value1 >= value2:
        return True
    else:
        return False

def isBig(value1, value2):
    if value1 > value2:
        return True
    else:
        return False


#if indi_2 all better(strongly), return True.  indiv1 is dominated by indiv2
def isDominated(indiv_1, indiv_2):
    fitness_method_list = msconfig.GLOBAL_VAR_OBJECT.FITNESS_METHOD_LIST
    counter_equalbig = 0
    counter_big = 0
    for fitness_method in fitness_method_list:
        if isEqualandBig(msfitness.getFitness(fitness_method, indiv_2), msfitness.getFitness(fitness_method, indiv_1)):
            counter_equalbig += 1
        if isBig(msfitness.getFitness(fitness_method, indiv_2), msfitness.getFitness(fitness_method, indiv_1)):
            counter_big += 1

    if counter_equalbig == len(fitness_method_list) and counter_big > 0:
        return True
    else:
        return False



#if indiv_1 dominate(all better than ) indiv_2, return True
def dominate(indiv_1, indiv_2):

    fitness_method_list = msconfig.GLOBAL_VAR_OBJECT.FITNESS_METHOD_LIST
    counter_big = 0
    counter_equalbig = 0
    for fitness_method in fitness_method_list:
        if isEqualandBig(msfitness.getFitness(fitness_method, indiv_1), msfitness.getFitness(fitness_method, indiv_2)):
            counter_equalbig += 1
        if isBig(msfitness.getFitness(fitness_method, indiv_1), msfitness.getFitness(fitness_method, indiv_2)):
            counter_big += 1

    if counter_equalbig == len(fitness_method_list) and counter_big > 0:
        return True
    else:
        return False


#for each indiv, compute the worseSet which is dominated by it. dominatedDict[indiv] = set
#compute  the better indiv number which dominate it.  isDominatedDict[indiv] = count
#return dominateSetDict[indiv1]=set(indiv,....)
#       isDominatedDict[indiv] = count
def initDominate(pop_list):
    dominateSetDict = dict()
    isDominatedDict = dict()
    for indiv in pop_list:
        #print("init tupe: ", myEncode(indiv)) #list cannot as a key, so use myEncode(list) as key
        dominateSetDict[myEncode(indiv)] = set()
        isDominatedDict[myEncode(indiv)] = 0

    for i in range(0, len(pop_list)):
        indiv_i = pop_list[i]
        for j in range(0, len(pop_list)):
            if i != j:
                indiv_j = pop_list[j]
                if isDominated(indiv_i, indiv_j):
                    if myEncode(indiv_i) not in isDominatedDict:
                        isDominatedDict[myEncode(indiv_i)] = 1
                    else:
                        isDominatedDict[myEncode(indiv_i)] += 1
                if dominate(indiv_i, indiv_j):
                    if myEncode(indiv_i) not in dominateSetDict:
                        dominateSetDict[myEncode(indiv_i)] = set()
                    dominateSetDict[myEncode(indiv_i)].add(myEncode(indiv_j))
    return dominateSetDict, isDominatedDict


#return layerList , and indiv's rank/layer number
def fastNondomSort(pop_list):
    [dominateSetDict, isDominatedDict] = initDominate(pop_list)
    #print 'dominateSetDict=', dominateSetDict
    #print 'isDominatedDict=', isDominatedDict
    layerList = list() #list[1] = [indiv1. ....]
    indivRankDict = dict() #[indiv] = rank
    #init F_list
    F_list = list()
    for indiv in pop_list:
        if isDominatedDict[myEncode(indiv)] == 0:
            F_list.append(myEncode(indiv))

    layer = 0
    while len(F_list) != 0:
        new_F_list = list()
        for indiv_i in F_list:
            oneset = dominateSetDict[indiv_i] #oneset
            #print("oneset:", oneset)
            for tuple_indiv_j in oneset:
                #print(tuple_indiv_j)
                isDominatedDict[tuple_indiv_j] -= 1
                if isDominatedDict[tuple_indiv_j] == 0:
                    new_F_list.append(tuple_indiv_j)
        #current layer save, and use a new layer
        layerList.append(F_list)
        F_list = new_F_list
        #print ('layer: ', layer, '=', layerList[layer])
        layer += 1
    #print ('quick nondoninate sort end..........')

    #decode ,generate the final layserList
    final_layer_list = list()
    for rank in range(0, len(layerList)):
        final_layer_list.append(list())
        for tuple_indiv in layerList[rank]:
            final_layer_list[rank].append(myDecode(tuple_indiv))
    #for rank in range(0, len(final_layer_list)):
    #    print ('layer: ', rank, '=', final_layer_list[rank])

    for rank in range(0, len(layerList)):
        for tuple_indiv in layerList[rank]:
            indivRankDict[tuple_indiv] = rank
    return final_layer_list, indivRankDict

#return the indiv's rank/layer
def getIndivRank(indiv, indivRankDict):
    return indivRankDict[myEncode(indiv)]

'''
alist=[ [0], [5, 2, 1, 6, 3], [7, 4]]
#alist = [[4], [44,"ff"], [66]]
atupe = myEncode(alist)
myDecode(atupe)
'''
