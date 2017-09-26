import random


def IsEqualIndiv(indivA, indivB):
    if indivA == indivB:
        return True
    else:
        return False

'''
def MakePair(selected_pop_list):
    #selected_pop_list = list(set(selected_pop_list)) #remove duplicate indiv,
    if len(selected_pop_list) <= 1:
        print 'selected_pop_list len = ', len(selected_pop_list)
    from itertools import combinations
    pairList = list(combinations(selected_pop_list, 2))
    return pairList


#parentPair,  N is the children needed
def RandomChooseParentPairs(parentPairList, N):
    if 2 * len(parentPairList) < N:
        print 'parents pairs are not enough...'
    if 2 * len(parentPairList) == N:
        return parentPairList

    #random delete the surplus partial element
    surplus = len(parentPairList) - N / 2
    for loop in range(0, surplus):
        index = random.randint(0, len(parentPairList) - 1)
        del parentPairList[index]
    return parentPairList
'''


def MakePairInOrder(selected_pop_list):
    parentPairList = list()  #[ [p1, p2],[p3, p4], ...]
    for index in range(0, len(selected_pop_list) / 2):
        parentPairList.append([selected_pop_list[2 * index], selected_pop_list[2 * index + 1]])
    return parentPairList

def FindFirstDiffIndex(str1, str2):
    for index in range(0, len(str1)):
        if str1[index] != str2[index]:
            return index
    return -1 #whole equal string

def CrossBySplitBit(strA, strB, start_cross_bit):
    rd = random.randint(start_cross_bit, len(strA) - 1) #randomly choose cross_start bit
    strA_part1 = strA[0:rd]
    strB_part1 = strB[0:rd]
    strA_part2 = strA[rd:len(strA)]
    strB_part2 = strB[rd:len(strB)]
    childA = strA_part1 + strB_part2
    childB = strB_part1 + strA_part2
    return childA, childB

#lenx is the X's len, leny is the y's len
def Crossover_2P2C(parentA, parentB, lenx, leny):
    parentA_x = parentA[0: lenx]
    parentA_y = parentA[lenx: lenx + leny]
    parentB_x = parentB[0: lenx]
    parentB_y = parentB[lenx: lenx + leny]
    x_start_cross_index = FindFirstDiffIndex(parentA_x, parentB_x)
    y_start_cross_index = FindFirstDiffIndex(parentA_y, parentB_y)

    if x_start_cross_index != -1:
        [childA_x, childB_x] = CrossBySplitBit(parentA_x, parentB_x, x_start_cross_index)
    else:
        childA_x = parentA_x
        childB_x = parentB_x

    if y_start_cross_index != -1:
        [childA_y, childB_y] = CrossBySplitBit(parentA_y, parentB_y, y_start_cross_index)
    else:
        childA_y = parentA_y
        childB_y = parentB_y

    childA = childA_x + childA_y
    childB = childB_x + childB_y
    return childA, childB


#N is thre children count needed
#lenList = [lenx, leny]
def Crossover(lenList, selected_pop_list, cross_operator):
    lenx = lenList[0]
    leny = lenList[1]

    new_pop_list = list()
    if cross_operator == '2P2C':
        #parentPairList = MakePair(selected_pop_list) #[ [str1,str2] [str2,str3] [str3,str4]....]
        #parentPairList = RandomChooseParentPairs(parentPairList, N)
        parentPairList = MakePairInOrder(selected_pop_list)
        for [parentA, parentB] in parentPairList:
            [childA, childB] = Crossover_2P2C(parentA, parentB, lenx, leny)
            new_pop_list.append(childA)
            new_pop_list.append(childB)
    elif cross_operator == '':
        print 'Unknown cross operator:', cross_operator

    return new_pop_list
