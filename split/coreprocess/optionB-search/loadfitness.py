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
            thr_int = int(float(thr) * 100)
            oneObjectStruct = ObjectStruct(int(nonlapClassCount), float(nonlapClassCount_avg), \
                            int(overlapClassCount), float(overlapClassCount_avg), \
                            int(realClusterNum), int(repeatClassCount), float(repeatClassCount_avg),\
                            int(interWorklow), int(withinWorkflow), int(interCallNum), float(interCallNum_avg), \
                            int(interCallNum_f), float(interCallNum_avg_f), int(APINum), float(APINum_avg))
            if serv not in objectStructDict:
                objectStructDict[serv] = dict()
            objectStructDict[serv][thr_int] = oneObjectStruct
    return objectStructDict
