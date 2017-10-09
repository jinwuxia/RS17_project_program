#for indiv in the same layer,
#compute indiv's crowd factor in its layer.

class IndivObject:
    def __init__(self, indiv, fitness_value):
        self.indiv = indiv
        self.fitness_value = fitness_value

#merge pop_list and fitness_list to be object_list.
#then sort from small to big
#return f_min, f_max, and sortedIndivObjectList
def SortThisLayer(pop_list, fitness_list):
    #merge
    objectList = list()
    for index in range(0, len(pop_list)):
        oneObject = IndivObject(pop_list[index], fitness_list[index])
        objectList.append(oneObject)
    #sort
    import operator
    cmpfunc = operator.attrgetter("fitness_value")
    objectList.sort(key = cmpfunc,  reverse = False)  #sheng xu

    f_min = objectList[0].fitness_value
    f_max = objectList[len(objectList) - 1].fitness_value
    return f_min, f_max, objectList

#compute crowd factor for all indivs in the layered pop
#ffrom layer to layer
def ComputeCrowd(layerList, fitnessMethodList):
    import fitness
    import config
    MAX_VALUE = 9999

    crowdDict = dict()  #[indiv] = crowdfactor
    for layer in range(0, len(layerList)):
        for indiv in  layerList[layer]:
            crowdDict[indiv] = 0

    for layer in range(0, len(layerList)):
        pop_list = layerList[layer]
        if len(pop_list) == 1:
            crowdDict[pop_list[0]] = MAX_VALUE
            continue
        for fitnessMethod in fitnessMethodList:
            fitness_list = fitness.GetFitnessList(fitnessMethod, pop_list)
            [fitness_min, fitness_max, sortedObjectList] = SortThisLayer(pop_list, fitness_list)
            #print 'compute crowd: pop_list=', pop_list
            #print 'compute crowd: fitness_list=', fitness_list
            #marin_left indiv
            crowdDict[sortedObjectList[0].indiv] = MAX_VALUE
            #margin_right indiv
            crowdDict[sortedObjectList[len(sortedObjectList) - 1].indiv] = MAX_VALUE
            #middle indiv
            for index in range(1, len(pop_list) - 1):
                indiv = sortedObjectList[index].indiv
                fitness_value = sortedObjectList[index].fitness_value
                if fitness_min != fitness_max:
                    det =  abs(sortedObjectList[index + 1].fitness_value - sortedObjectList[index - 1].fitness_value) / float(fitness_max - fitness_min)
                else:
                    det = abs(sortedObjectList[index + 1].fitness_value - sortedObjectList[index - 1].fitness_value)
                crowdDict[indiv] += det
    return crowdDict


def GetIndivCrowd(indiv, indivCrowdDict):
    return indivCrowdDict[indiv]
