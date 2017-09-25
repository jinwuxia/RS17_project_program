
#10 jin zhi to 2 jin zhi
def Dec2bit(number, bitCount):
    if number == 0:
        strList = ['0'] * bitCount
    else:
        strList = ['0'] * bitCount
        index = len(strList) - 1
        while(number != 0):
            shang = number / 2
            yushu = number % 2
            strList[index] = str(yushu)
            index -= 1
            number = shang
    return ''.join(strList)



#N is the population size, pop0_list is the individual list.
#pop0_list[i] = 'xxxxxxxx'
#x=[x_s, x_e] = [1,10]
#y=[y_s, y_e] = [1, 100]
def InitPop(N, x_s, x_e, y_s, y_e):
    pop_list = list()
    import random
    for index in range(0, N):
        #x=[1,1,2,...,10]
        xi = random.randint(x_s, x_e)
        #y=[1,2,...,100]
        yi = random.randint(y_s, y_e)

        xibit = Dec2bit(xi, bitCount=4)
        yibit = Dec2bit(yi, bitCount=7)
        oneStr = xibit + yibit
        pop_list.append(oneStr)
        print xi, xibit, yi, yibit
    return  pop_list

#compute one ondividual's fitness value.
def Fitness(oneIndiv):
    return fitness_value

#selected better parents by using Probility of fitness_function_value
#pop_list and fitness_value_list are corresponding
def SelectPop_Pro(pop_list, fitness_value_list, probability):
    selected_pop_list = list()

    fenmu = sum(fitness_value_list)
    pro_list = [each / float(fenmu) for each in fitness_value_list]
    for index in len(0, len(pop_list)):
        if pro_list[index] >= probability:
            selected_pop_list.append(pop_list[index])

    if len(selected_pop_list) / 2 == 1:  #if is even, repeate one randomly
        import random
        rindex = random.randint(0, len(selected_pop_list) - 1)
        selected_pop_list.append(selected_pop_list[rindex])
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
        if e_new < e_old:   #p=1 accepted
            selected_pop_list.append(new_pop_list[index])
        else:
            detE = -(e_new - e_old)
            accept_bad_pro = min(1, math.exp(detE/float(t)))
            p = random(0, 1)
            if p <= accept_bad_pro:  #accept
                selected_pop_list.append(new_pop_list[index])
            else:
                selected_pop_list.append(old_pop_list[index])

    return selected_pop_list




def Crossover(selected_pop_list, cross_operator):
    if cross_operator == '':
    elif cross_operator == '':

    return new_pop_list


def Mutation(new_pop_list):

    return mutation_pop_list


#judge the search iteration condition
def IsStop():
    return True


def MainFunc():
    #step1: init population
    N = 6 #initial populization size
    x_s = 1
    x_e = 10
    y_s = 1
    y_e = 100

    selected_method = 'PRO'  #PRO or SA
    tem = 100
    cooling_rate = 0.98

    cross_operator = ''


    pop_list = InitPop(N, x_s, x_e, y_s, y_e)

    old_pop_list = list()
    old_fitness_value_list = list()
    while(True):
        #step2: compute finess
        fitness_value_list = list()
        for index  in range(0, len(pop_list)):
            indiv = pop_list[index]
            fitness_value_list[index] = Fitness(indiv)

        #step3: select better ones as parents for reproduction
        if selected_method == 'PRO':
            selected_pop_list = SelectPop_Pro(pop_list, fitness_value_list)
        elif selected_method == 'SA':
            if len(old_pop_list) == 0:
                selected_pop_list = SelectPop_Pro(pop_list, fitness_value_list)
            else:
                selected_pop_list = SelectPop_SA(pop_list, fitness_value_list, old_pop_list, old_fitness_value_list, tem)
                tem = tem * cooling_rate
        else:
            print 'Unknown selecting method: ', selected_method

        #step4: crossover by using selected_pop, generate new generation
        new_pop_list = Crossover(selected_pop_list, cross_operator)

        #step5: muatition in a small probability
        new_pop_list = Mutation(new_pop_list)

        #record states
        old_pop_list = selected_pop_list  #old, parents
        pop_list = new_pop_list  #new, children
        old_fitness_value_list = fitness_value_list  #old

        if IsStop() == True:
            break
