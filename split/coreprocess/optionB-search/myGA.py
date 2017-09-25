
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

#pop_list and fitness_value_list are corresponding
def SelectPop(kgen, pop_list, fitness_value_list):
    return seleted_pop_list


def Crossover(selected_pop_list):
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
    pop_list = InitPop(N, x_s, x_e, y_s, y_e)

    kgen = 0 #generation = K
    while(True):
        #step2: compute finess
        fitness_value_list = list()
        for index  in range(0, len(pop_list)):
            indiv = pop_list[index]
            fitness_value_list[index] = Fitness(indiv)

        #step3: select better ones as parents for reproduction
        selected_pop_list = SelectPop(kgen, pop_list, fitness_value_list)

        #step4: crossover by using selected_pop, generate new generation
        new_pop_list = Crossover(selected_pop_list)

        #step5: muatition in a small probability
        new_pop_list = Mutation(new_pop_list)

        #record states
        kgen += 1
        pop_list = new_pop_list

        if IsStop() == True:
            break
