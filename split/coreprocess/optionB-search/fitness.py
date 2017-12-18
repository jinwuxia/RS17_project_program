#compute one ondividual's fitness value.

#compute one ondividual's fitness value.

class ObjectStruct:
    def __init__(self, servnum, nonlapClassCount, nonlapClassCount_avg, overlapClassCount, overlapClassCount_avg, \
                    realClusterNum, repeatClassCount, repeatClassCount_avg,\
                    interWorklow, withinWorkflow, interCallNum, interCallNum_avg, \
                    interCallNum_f, interCallNum_avg_f, APINum, APINum_avg):
        self.servnum = servnum
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
            #print each
            if serv == 'servicenumber':
                continue
            serv = int(serv)
            thr_int = int(thr)
            oneObjectStruct = ObjectStruct(serv, int(nonlapClassCount), float(nonlapClassCount_avg), \
                            int(overlapClassCount), float(overlapClassCount_avg), \
                            int(realClusterNum), int(repeatClassCount), float(repeatClassCount_avg),\
                            int(interWorklow), int(withinWorkflow), int(interCallNum), float(interCallNum_avg), \
                            int(interCallNum_f), float(interCallNum_avg_f), int(APINum), float(APINum_avg))
            if serv not in objectStructDict:
                objectStructDict[serv] = dict()
            objectStructDict[serv][thr_int] = oneObjectStruct
    config.set_object_struct(objectStructDict)

def loadFitness_noRepeat(fileName):
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
            #print each
            if serv == 'servicenumber':
                continue
            serv = int(serv)
            thr_int = int(thr)
            if int(repeatClassCount) == 0:
                oneObjectStruct = ObjectStruct(serv, int(nonlapClassCount), float(nonlapClassCount_avg), \
                            int(overlapClassCount), float(overlapClassCount_avg), \
                            int(realClusterNum), int(repeatClassCount), float(repeatClassCount_avg),\
                            int(interWorklow), int(withinWorkflow), int(interCallNum), float(interCallNum_avg), \
                            int(interCallNum_f), float(interCallNum_avg_f), int(APINum), float(APINum_avg))
                if serv not in objectStructDict:
                    objectStructDict[serv] = dict()
                objectStructDict[serv][thr_int] = oneObjectStruct
    config.set_object_struct(objectStructDict)

#make min to max. All the object should be maximized
def GetFitnessList(fitness_method, pop_list):
    import config
    import initpop
    OBJECT_STRUCT_DICT = config.get_object_struct()
    BIT_COUNT_X = config.GlobalVar.BIT_COUNT_X
    BIT_COUNT_Y = config.GlobalVar.BIT_COUNT_Y
    X_S = config.GlobalVar.X_S
    X_E = config.GlobalVar.X_E
    Y_S = config.GlobalVar.Y_S
    Y_E = config.GlobalVar.Y_E

    fitness_value_list = list()
    for index  in range(0, len(pop_list)):
        indiv = pop_list[index]
        [x, y] = initpop.TransCode2Indiv(indiv, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)  #=[x,y]=[serv, thr_int]
        #print 'info fit[x][y]:', x, y
        if fitness_method == 'servnum':
            fitness_value_list.append(OBJECT_STRUCT_DICT[x][y].servnum)
        elif fitness_method == 'withinwf':
            fitness_value_list.append(OBJECT_STRUCT_DICT[x][y].withinWorkflow)
        elif fitness_method == 'clusternum':
            fitness_value_list.append(OBJECT_STRUCT_DICT[x][y].realClusterNum)
        elif fitness_method == 'repclassnum':
            fitness_value_list.append(-OBJECT_STRUCT_DICT[x][y].repeatClassCount)
        elif fitness_method == 'withinwf-interwf-repclass':
            fitness_value_list.append(OBJECT_STRUCT_DICT[x][y].withinWorkflow \
                                    - OBJECT_STRUCT_DICT[x][y].interWorklow \
                                    - OBJECT_STRUCT_DICT[x][y].repeatClassCount)
        else:
            print 'Unknown fitness_method:', fitness_method
    return fitness_value_list

def GetFitness(fitness_method, indiv):
    import config
    import initpop
    OBJECT_STRUCT_DICT = config.get_object_struct()
    BIT_COUNT_X = config.GlobalVar.BIT_COUNT_X
    BIT_COUNT_Y = config.GlobalVar.BIT_COUNT_Y
    X_S = config.GlobalVar.X_S
    X_E = config.GlobalVar.X_E
    Y_S = config.GlobalVar.Y_S
    Y_E = config.GlobalVar.Y_E

    [x, y] = initpop.TransCode2Indiv(indiv, X_S, X_E, Y_S, Y_E, BIT_COUNT_X, BIT_COUNT_Y)  #=[x,y]=[serv, thr_int]
    #print 'info fit[x][y]:', x, y
    if fitness_method == 'servnum':
        fitness_value = OBJECT_STRUCT_DICT[x][y].servnum
    elif fitness_method == 'withinwf':
        fitness_value = OBJECT_STRUCT_DICT[x][y].withinWorkflow
    elif fitness_method == 'clusternum':
        fitness_value = OBJECT_STRUCT_DICT[x][y].realClusterNum
    elif fitness_method == 'repclassnum':
        fitness_value = (-OBJECT_STRUCT_DICT[x][y].repeatClassCount)
    elif fitness_method == 'withinwf-interwf-repclass':
        fitness_value = OBJECT_STRUCT_DICT[x][y].withinWorkflow \
                                    - OBJECT_STRUCT_DICT[x][y].interWorklow \
                                    - OBJECT_STRUCT_DICT[x][y].repeatClassCount
    else:
        print 'Unknown fitness_method:', fitness_method
    return fitness_value
