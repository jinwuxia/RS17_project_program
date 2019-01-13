import sys
import csv
import math

def computeDistance(fit_list1, fit_list2):
    n = len(fit_list1)
    sum = 0
    for i in range(0, n):
        x = fit_list1[i]
        y = fit_list2[i]
        sum += (x-y) * (x-y)
    return math.sqrt(sum)

#[solution_index, fit1, fit2, ..., fit4]
def choosebest(fitness_result):
    fit1_list = list()
    fit2_list = list()
    fit3_list = list()
    fit4_list = list()
    idea_fit = list()
    pop_fitness = list() #[solution index] = [fit1, ...., fit4]

    for each in fitness_result:
        [solution_index, fit1, fit2, fit3, fit4] = each
        pop_fitness.append([fit1, fit2, fit3, fit4])
        fit1_list.append(fit1)
        fit2_list.append(fit2)
        fit3_list.append(fit3)
        fit4_list.append(fit4)

    idea_fit = [max(fit1_list), max(fit2_list), max(fit3_list), max(fit4_list) ]

    # The knee point is the neasrest point from the idea points
    distance_list = list()
    for solution_index in range(0, len(pop_fitness)):
        distance = computeDistance(pop_fitness[solution_index], idea_fit)
        distance_list.append(distance)
    res = distance_list.index(min(distance_list))
    #print('all distance:', distance_list)
    #print("idea point:", idea_fit)
    #print("knee point: ", res, pop_fitness[res], "  distance:", min(distance_list) )
    return res

def readFitness(filename):
    fit1_list = list()
    fit2_list = list()
    fit3_list = list()
    fit4_list = list()
    idea_fit = list()
    pop_fitness = list() #[solution index] = [fit1, ...., fit4]
    with open(filename, "r", newline = "") as fp:
        reader = csv.reader(fp)
        for each in reader:
            [solution_index, fit1, fit2, fit3, fit4] = each
            fit1 = float(fit1)
            fit2 = float(fit2)
            fit3 = float(fit3)
            fit4 = float(fit4)
            pop_fitness.append([fit1, fit2, fit3, fit4])
            fit1_list.append(fit1)
            fit2_list.append(fit2)
            fit3_list.append(fit3)
            fit4_list.append(fit4)

    idea_fit = [max(fit1_list), max(fit2_list), max(fit3_list), max(fit4_list) ]

    # The knee point is the neasrest point from the idea points
    distance_list = list()
    for solution_index in range(0, len(pop_fitness)):
        distance = computeDistance(pop_fitness[solution_index], idea_fit)
        distance_list.append(distance)
    res = distance_list.index(min(distance_list))
    print('all distance:', distance_list)
    print("idea point:", idea_fit)
    print("knee point: ", res, pop_fitness[res], "  distance:", min(distance_list) )


#readFitness(sys.argv[1])

'''
fit_list1=[3,4,5]
fit_list2=[4,5,6]
value = computeDistance(fit_list1, fit_list2)
print(value)
'''
