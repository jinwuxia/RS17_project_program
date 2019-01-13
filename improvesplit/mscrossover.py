import random
'''
the single-parent producing children are finished.
two-parents producing two children are TBA
'''


def makePairInOrder(pop_list):
    return list()

def crossover_2P2C(parentA, parentB):
    childA = list()
    childB = list()
    return childA, childB



#classify  candidate into two types. one type that can be splitted due to size of larger than 1
def categorizeCandidate(parent):
    selectedCandidates = list()
    otherCandidates = list()
    for candidate in parent:
        if len(candidate) >= 2:
            selectedCandidates.append(candidate)
        else:
            otherCandidates.append(candidate)
    return selectedCandidates, otherCandidates

#reproduce by one parent= individual
#generate a partition neibour
#random select a candidate which has more than one atoms
#random move one atom from this candidate to other one candidate.
#the children number is equal to the number of candidates - 1.
def crossover_1PNC(parent):
    #print("parent: ", parent)
    childrenList = list()
    [selectedCandidates, otherCandidates] = categorizeCandidate(parent)
    #random select a candidate to split
    split_candidate_index = random.randint(0, len(selectedCandidates) - 1)
    #other candidates that will be updated by adding the following atom
    for index in range(0, len(selectedCandidates)):
        if index != split_candidate_index:
            otherCandidates.append(selectedCandidates[index])
    #print("otherCandidates before moving:", otherCandidates)
    #let's split the candidate = selectedCandidates[split_candidate_index]
    #random select a atom which will be moved out.
    #candidate = [atom1, atom2,..]
    splitCandidate = selectedCandidates[split_candidate_index]
    atom_index = random.randint(0, len(splitCandidate) - 1)
    moved_atom_id = splitCandidate[atom_index]
    #print("the split candidate:", splitCandidate)
    #print("the moved atom:", moved_atom_id)

    new_splitCandidate = splitCandidate[:]
    del new_splitCandidate[atom_index]
    #print("otherCandidates are moving:", otherCandidates)

    for index in range(0, len(otherCandidates)):
        child = list()

        child.append(new_splitCandidate) #the splitted candidate

        new_othercandidate = otherCandidates[index][:] #copy deeep,, otherwise will both changed
        new_othercandidate.append(moved_atom_id)
        #print("updated candidate:", otherCandidates[index], new_othercandidate)
        child.append(new_othercandidate) #the moved in candidate

        for index2 in range(0, len(otherCandidates)):
            if index2 != index:
                child.append(otherCandidates[index2]) # other candidate will not be changed.
        childrenList.append(child)
        #print("a child: ", child)

    return childrenList

#random choose n from list
def randomChoose(alist, N):
    newList = list()
    newIndexList = list()
    max_index = len(alist) - 1

    while (len(newList) < N):
        index = random.randint(0, max_index)
        if index not in newIndexList:
            newIndexList.append(index)
            newList.append(alist[index])
    return newList

'''
crossover, generate children
when using 1PNC, the children will be  greater
so if parent candidate size > 30, the random choose 20 as children
'''
def crossover(pop_list,  cross_operator):
    new_pop_list = list()
    if cross_operator == '2P2C':
        #[ [str1,str2] [str2,str3] [str3,str4]....]
        parentPairList = makePairInOrder(pop_list)
        for [parentA, parentB] in parentPairList:
            [childA, childB] = crossover_2P2C(parentA, parentB)
            new_pop_list.append(childA)
            new_pop_list.append(childB)
    elif cross_operator == "1PNC":
        for parent in pop_list:
            children = crossover_1PNC(parent)
            if len(parent) > 20 and len(children) > 20:  #when parent'candidate size > 20 and  all children of this gen >20
                children = randomChoose(children, 4)  #limit the children is 20
            new_pop_list.extend(children)

    else:
        print ('Unknown cross operator:', cross_operator)
    return new_pop_list


#test method
def test_crossover():
    #test
    indiv1 = [[7, 3, 6, 5, 0], [8], [1, 2, 4, 9]]
    indiv2 = [[8, 6, 9, 0], [3, 5, 1, 4], [2, 7]]
    pop_list=[indiv1, indiv2]
    cross_operator = "1PNC"
    new_pop_list = crossover(pop_list,  cross_operator)
    for indiv in new_pop_list:
        print(indiv)
