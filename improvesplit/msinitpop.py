from random import shuffle
import random


 #each service candidate is a list of atom.
 #each indiv (pattiton ) is a list of candidate

'''
pop_number: is the size of populations
candidateNumber: is the service number

random generate services with candidateNumber for popluation
'''
def init_pop(atom_number, pop_number, candidateNumber):
    pop_list = list()
    for index in range(0, pop_number):
        indiv = genIndivRandom(atom_number, candidateNumber)
        pop_list.append(indiv)
    return pop_list


'''
generate a list from 0 to atomsize-1
shuffle the list
random generate different number in candidateNumber-1 times
add bound =0
add bound = atomsize
'''
def genIndivRandom(atom_number, candidateNumber):
    alist = list()
    for i in range(0, atom_number):
        alist.append(i)
    shuffle(alist) #shuffle in place
    #print("shuffle list: ", alist)

    time = 1
    partitionIndexList = list()
    while time < candidateNumber:
        x = random.randint(1,  atom_number - 2)# randint(a,b): a<=x<=b
        while x in partitionIndexList:
            x = random.randint(1,  atom_number - 2)# randint(a,b): a<=x<=b
        time += 1
        partitionIndexList.append(x)

    partitionIndexList.append(0) #last bound
    partitionIndexList.append(atom_number) #last bound
    partitionIndexList.sort() #sort in place

    #print("partition bound: ", partitionIndexList)

    indiv = list() #each service candidate is a list
    index1 = partitionIndexList[0] #first bound
    del partitionIndexList[0]
    #index1-index2 is a subset of the parttion
    for index2 in partitionIndexList:
        sublist = list()
        for i in range(index1, index2):
            sublist.append(alist[i])
        #print("sublist:", sublist)
        index1 = index2
        indiv.append(sublist)
    #print("indiv: ", indiv)
    return indiv


#test the init pop
def test_init_pop():
    atom_number = 10
    candidateNumber = 3
    pop_number = 5
    #genIndivRandom(atom_number, candidateNumber)
    pop_list = init_pop(atom_number, pop_number, candidateNumber)
    print("init pop: ")
    for each in pop_list:
        print (each)

#test_init_pop()
