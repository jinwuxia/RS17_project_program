
#selected better parents by using Probility of fitness_function_value
#pop_list and fitness_value_list are corresponding
def SelectPop_Pro(pop_list, fitness_value_list, probability):
    selected_pop_list = list()

    fenmu = sum(fitness_value_list)
    pro_list = [each / float(fenmu) for each in fitness_value_list]
    print 'probability: ', pro_list
    for index in range(0, len(pop_list)):
        if pro_list[index] >= probability:
            selected_pop_list.append(pop_list[index])

    if len(selected_pop_list) % 2 == 1:  #if is even, repeate one randomly, generate one for the last element
        import random
        rindex = random.randint(0, len(selected_pop_list) - 2)
        selected_pop_list.append(selected_pop_list[rindex])

    #print 'selected_pop_list:', selected_pop_list
    return selected_pop_list

#selected better parents by using simulated annealing
#pop_list and fitness_value_list are corresponding
def SelectPop_SA(new_pop_list, new_fitness_value_list, old_pop_list, old_fitness_value_list, t):
    #Old and new are same size
    import math
    import random
    selected_pop_list = list()
    for index in range(0, len(new_pop_list)):
        e_new = new_fitness_value_list[index]
        e_old = old_fitness_value_list[index]
        if e_new >= e_old:   #p=1 accepted
            selected_pop_list.append(new_pop_list[index])
        else:
            detE = (e_new - e_old)
            accept_bad_pro = min(1, math.exp(detE/float(t)))
            print 'detE=', detE, 'math.exp(detE/float(t))=', math.exp(detE/float(t)), 'accepted_bad_pro=', accept_bad_pro
            p = random.random()
            if p <= accept_bad_pro:  #accept
                print 'SA accpted bad, p=', p
                selected_pop_list.append(new_pop_list[index])
            else:
                selected_pop_list.append(old_pop_list[index])

    return selected_pop_list

#randomly choose n from m, then select the top k from m.
#M >= N
def RandomChoose(m, n, k):
    resList = list()
    if n> m or k > n:
        print 'Not enough m,n,k.....'
        return resList

    import random
    aList = list()
    for index in range(0, n):
        number = random.randint(0, m-1)
        aList.append(number)
    #sort aList
    aList.sort() #from small to big
    for index in range(0, k):
        resList.append(aList[index])
    return resList


#according to the sorted Pop_listm select parentA_list and parentB_list
#2 * N <= pop_list_number
# each time randomly choose M from len(layerList), then choose top N from M
def SelectPop_Jinbiao(layerList, M, N):
    print layerList
    parentA_list = list()
    parentB_list = list()
    flatList = list()
    for layer in range(0, len(layerList)):
        flatList.extend(layerList[layer])
    while len(flatList) < 2* N:
        print 'not enough pop_list to generate ', N, 'pairs parents....'
        N=  len(flatList) / 2
        M = N - 2
    else:
        parentA_index_list = RandomChoose(len(flatList), M, N)
        for index in parentA_index_list:
            parentA_list.append(flatList[index])
        parentB_index_list = RandomChoose(len(flatList), M, N)
        for index in parentB_index_list:
            parentB_list.append(flatList[index])

    return parentA_list, parentB_list
