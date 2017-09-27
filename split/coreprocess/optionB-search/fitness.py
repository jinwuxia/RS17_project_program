#compute one ondividual's fitness value.

#compute one ondividual's fitness value.

class ObjectStruct:
    def __init__(self, nonlapClassCount, nonlapClassCount_avg, overlapClassCount, overlapClassCount_avg, \
                    realClusterNum, repeatClassCount, repeatClassCount_avg,\
                    interWorklow, withinWorkflow, interCallNum, interCallNum_avg, \
                    interCallNum_f, interCallNum_avg_f, APINum, APINum_avg):
        self.nonlapClassCount = nonlapClassCount
        self.nonlapClassCount_avg = nonlapClassCount_avg
        self.overlapClassCount = overlapClassCount
        self.overlapClassCount_avg = overlapClassCount_avg
        self.realClusterNum = realClusterNum
        self.repeatClassCount = repeatClassCount
        self.repeatClassCount_avg  =repeatClassCount_avg
        self.interWorklow = interWorklow
        self.withinWorkflow = withinWorkflow
        self.interCallNum = interCallNum
        self.interCallNum_avg = interCallNum_avg
        self.interCallNum_f = interCallNum_f
        self.interCallNum_avg_f = interCallNum_avg_f
        self.APINum = APINum
        self.APINum_avg = APINum_avg

def loadFitness(fileName):
    import config
    objectStructDict = dict()
    import csv
    with open(fileName, 'rb') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [serv, thr, nonlapClassCount, nonlapClassCount_avg, overlapClassCount, overlapClassCount_avg, \
            highLap, highLap_avg, lowLap, lowLap_avg, \
            realClusterNum, repeatClassCount, repeatClassCount_avg,\
            interWorklow, withinWorkflow, interCallNum, interCallNum_avg, \
            interCallNum_f, interCallNum_avg_f, APINum, APINum_avg]     = each
            if serv == 'servicenumber':
                continue
            serv = int(serv)
            thr_int = int(thr)
            oneObjectStruct = ObjectStruct(int(nonlapClassCount), float(nonlapClassCount_avg), \
                            int(overlapClassCount), float(overlapClassCount_avg), \
                            int(realClusterNum), int(repeatClassCount), float(repeatClassCount_avg),\
                            int(interWorklow), int(withinWorkflow), int(interCallNum), float(interCallNum_avg), \
                            int(interCallNum_f), float(interCallNum_avg_f), int(APINum), float(APINum_avg))
            if serv not in objectStructDict:
                objectStructDict[serv] = dict()
            objectStructDict[serv][thr_int] = oneObjectStruct
    config.set_object_struct(objectStructDict)


def GetFitnessList(FITNESS_METHOD, pop_list, BIT_COUNT_X, BIT_COUNT_Y):
    import config
    import initpop
    OBJECT_STRUCT_DICT = config.get_object_struct()
    fitness_value_list = list()
    for index  in range(0, len(pop_list)):
        indiv = pop_list[index]
        [x, y] = initpop.TransCode2Indiv(indiv, BIT_COUNT_X, BIT_COUNT_Y)  #=[x,y]=[serv, thr_int]
        print 'info fit[x][y]:', x, y
        if FITNESS_METHOD == 'withinwf':
            fitness_value_list.append(OBJECT_STRUCT_DICT[x][y].withinWorkflow)
        elif FITNESS_METHOD == 'withinwf-interwf-repclass':
            fitness_value_list.append(OBJECT_STRUCT_DICT[x][y].withinWorkflow \
                                    - OBJECT_STRUCT_DICT[x][y].interWorklow \
                                    - OBJECT_STRUCT_DICT[x][y].repeatClassCount)
        else:
            print 'Unknown fitness_method:', FITNESS_METHOD
    return fitness_value_list
