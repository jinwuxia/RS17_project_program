import sys
import msconfig
import msloaddata
import msinitpop
import msfitness
import msselect
import mscrossover
import msmutation
import mscrowdfactorcal
import csv
import msmetric



def isStop(gen_k):
    if gen_k > msconfig.GLOBAL_VAR_OBJECT.MAX_ITERATION_LOOP:
        return True
    '''
    #is stable
    if toSet(current_knee_point) == toSet(msconfig.get_current_knee_point()):
        msconfig.add_continue_best_loop()  #crrrent + 1
    else:
        msconfig.reset_continue_best_loop()#reset current = 0
    if msconfig.get_continue_best_loop() > msconfig.GLOBAL_VAR_OBJECT.CONTINUE_BEST_LOOP:
        return True
    '''
    return False

def prepare(atomfileName, calldepFile, concerndepFile):
    [classIDNameDict, classNameIDDict, allAtoms] = msloaddata.loadAtomData(atomfileName)
    msconfig.set_allatom_list(allAtoms)
    msconfig.set_classidname_dict(classIDNameDict)
    msconfig.set_classnameid_dict(classNameIDDict)

    classDepDict = msloaddata.loadDepData(calldepFile, concerndepFile)
    msconfig.set_classfinaldep_dict(classDepDict)
    print("laod data end...")


def nsga_process():
    res_pop_list = list()
    knee_point = list()
    pop_size = msconfig.GLOBAL_VAR_OBJECT.POP_SIZE
    candidate_number =  msconfig.GLOBAL_VAR_OBJECT.PARTITION_K
    parent_number = msconfig.GLOBAL_VAR_OBJECT.PARENT_M
    cross_operator = msconfig.GLOBAL_VAR_OBJECT.CROSSOVER_OPERATOR
    mutation_operator = msconfig.GLOBAL_VAR_OBJECT.MUTATION_OPERATOR
    mutation_probabilty = msconfig.GLOBAL_VAR_OBJECT.MUTATION_PROBABILITY
    fitness_method_list = msconfig.GLOBAL_VAR_OBJECT.FITNESS_METHOD_LIST

    atom_number = len(msconfig.get_allatom_list())
    initial_pop_list = msinitpop.init_pop(atom_number, pop_size, candidate_number)
    #print("init the pop")
    #for indiv in initial_pop_list:
    #    print(indiv)

    this_pop_list = initial_pop_list
    last_pop_list = list()
    gen_k = 1
    while True:
        if gen_k == 1:
            msmetric.computeFitnessThread(this_pop_list, fitness_method_list)
            parent_pop_list = msselect.selectParentsByLayer(this_pop_list, parent_number)
        else:
            #msmetric.computeFitnessThread(this_pop_list, fitness_method_list)
            parent_pop_list = msselect.selectParentsByElicit(this_pop_list, parent_number)
        print("select out as the parent:")
        #for each in parent_pop_list:
        #    print(each)

        #print ("generate children..")
        children = mscrossover.crossover(parent_pop_list,  cross_operator)
        children = msmutation.mutation(children, mutation_operator, mutation_probabilty)

        last_pop_list = this_pop_list[:]
        print("the population of Gen  ", gen_k)
        this_pop_list = list()
        this_pop_list.extend(parent_pop_list)
        this_pop_list.extend(children)
        #delete the duplicate
        print("before len: ", len(this_pop_list))
        this_pop_list = removeDuplicate(this_pop_list)
        print("after len: ", len(this_pop_list))
        gen_k += 1

        msmetric.computeFitnessThread(this_pop_list,fitness_method_list)
        res_pop_list = msselect.selectParentsByLayer(this_pop_list, parent_number)
        #[knee_point, knee_fit] = getKneePoint(res_pop_list)
        if isStop(gen_k):
            break
        else:
            pass
            #msconfig.set_current_knee_point(knee_point)
    #end while
    return res_pop_list#, knee_point, knee_fit


def getKneePoint(pop_list):
    resList = list()
    for index in range(0, len(pop_list)):
        indiv = pop_list[index]
        tmp = list()
        tmp.append(index)
        for fitness_method in msconfig.GLOBAL_VAR_OBJECT.FITNESS_METHOD_LIST:
            fit = msfitness.getFitness(fitness_method, indiv)
            tmp.append(fit)
        resList.append(tmp)
    import msknee
    index = msknee.choosebest(resList)
    print("best solution:", pop_list[index])
    print("best fitness:", resList[index])
    return pop_list[index], resList[index]

def toSet(indiv):
    aset = set()
    for candidate in indiv:
        each = frozenset(candidate)
        aset.add(each)
    return aset


def removeDuplicate(pop_list):
    new_pop_list = list()
    set_list = list()
    for indiv in pop_list:
        aset = toSet(indiv)
        if aset not in set_list:
            new_pop_list.append(indiv)
            set_list.append(aset)
    return new_pop_list


#{frozen(1,2), frozen()}
#indivset, indiv is a set of frozenset
def getPartionResult(indivset):
    allAtoms = msconfig.get_allatom_list()
    classID2NameDict = msconfig.get_classidname_dict()

    resList = list()
    candidateId = 0
    for candidate in indivset:
        classSet = set()
        for atomId in candidate:
            tmp = allAtoms[atomId].classIdSet
            classSet.update(tmp)
        for classId in classSet:
            classname = classID2NameDict[classId]
            alist = ["contain", candidateId, classname]
            resList.append(alist)
        candidateId += 1
    return resList

def writeCSV(alist, filename):
    with open(filename, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(alist)


if __name__ == "__main__":
    atomfileName = sys.argv[1]
    calldepFile = sys.argv[2]
    concerndepFile = sys.argv[3]
    project= sys.argv[4]
    fitnesslogfile = sys.argv[5]
    candidate_number =  msconfig.GLOBAL_VAR_OBJECT.PARTITION_K

    prepare(atomfileName, calldepFile, concerndepFile)

    for i in range(0, msconfig.GLOBAL_VAR_OBJECT.REPEAT_TIMES):
        print("iteration: ", i)
        #[pop_list, knee_point, knee_fit] = nsga_process()
        pop_list = nsga_process()
        k = 0
        for each in pop_list:
            filename = project + "_fome_" + str(candidate_number) + "_iter_" + str(i) + "_k" + str(k) + ".csv"
            alist = getPartionResult(toSet(each))
            writeCSV(alist, filename)
            k+= 1
            #if toSet(each) == toSet(knee_point):
            #    print(filename, " is knee files....")
