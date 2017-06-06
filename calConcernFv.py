import sys
import csv

CLASSDict = dict()   #classDoct[classID] = className

def ReadCSV(fileName):
    resList = list()
    with open(fileName, "rb") as fp:
        reader = csv.reader(fp, delimiter = ',')
        for eachLine in reader:
            resList.append(eachLine)
    return resList

	
def WriteCSV(fileName,listlist):
    print fileName
    with open(fileName, "wb") as fp:
        writer = csv.writer(fp)
        writer.writerow(['From Class', 'To Class', 'Semantic_Sim'])
        for i in range(0, len(listlist)):
            for j in range(0, len(listlist)):
                if i != j:
                    writer.writerow( [CLASSDict[i], CLASSDict[j], "%.4f" % listlist[i][j] ])
            

			
def IsLess(floatNum, threshold):
    if floatNum - threshold <= 0.001:
        return True
    else:
        return False

		
def IsEqual(floatNum1, floatNum2):
    if abs(floatNum1 - floatNum2) <= 0.0001:
        return True
    else:
        return False


# read fv and normalize them
def DelAndNormalize(fv):
    newFv = list()
    minList = list()
    maxList = list()
    #print fv
    classIndex = 0
    for eachList in fv:
        className = eachList[0]
        CLASSDict[classIndex] = className
        del eachList[0]
        classIndex += 1
     
        for index in range(0, len(eachList)):
            eachList[index] = float(eachList[index])
       
        newFv.append(eachList)
        minList.append(min(eachList))
        maxList.append(max(eachList))
    minValue = min(minList)
    maxValue = max(maxList)
    print "min= ", minValue, ";  maxValue = ", maxValue

    for i in range(0, len(newFv)):
        for j in range(0, len(newFv[i])):
            newFv[i][j] = (newFv[i][j] - minValue)  / float(maxValue - minValue)

    return newFv



#find the differ between two feature vector
def FindDiffer(vector_i, vector_j, thr):
    bothIndex = list()
    onlyBIndex = list()
    onlyAIndex = list()
    bothNotIndex = list()
    bothVal = list()
    onlyBVal = list()
    onlyAVal = list()
    bothNotVal = list()

    n = len(vector_i) #  len(vector_i) = len(vector_j)
    #notice: elment of vector is float, how to compare float with 0
    for index in range(0, n): #list=[0,1,..., n-1]
        if not IsLess(vector_i[index], thr)  and  not IsLess(vector_j[index], thr):
            bothIndex.append(index)
            bothVal.append(vector_i[index] + vector_j[index])
        elif IsLess(vector_i[index], thr) and not IsLess(vector_j[index], thr):
            onlyBIndex.append(index)
            onlyBVal.append(vector_j[index])
        elif not IsLess(vector_i[index], thr) and IsLess(vector_j[index], thr):
            onlyAIndex.append(index)
            onlyAVal.append(vector_i[index])
	elif IsLess(vector_i[index], thr) and  IsLess(vector_j[index], thr):
            bothNotIndex.append(index)
            bothNotVal.append(vector_i[index])

    return bothIndex, onlyAIndex, onlyBIndex, bothNotIndex, bothVal, onlyAVal, onlyBVal, bothNotVal


#for this distance, the more, the marrier
def CalDistClassij(i, j, class1Fv, class2Fv, distFunc, thr):
    if i == j:
        return 0

    if len(class1Fv) != len(class2Fv):
        print "this two feature vector donnot have same len\n"
        return

    [bothIndex, onlyAIndex, onlyBIndex, bothNotIndex, bothVal, onlyAVal, onlyBVal, bothNotVal] = FindDiffer(class1Fv, class2Fv, thr ) #aIndex is the index array
    if distFunc == "jm":
        fenzi = len(bothIndex)
        fenmu = len(bothIndex) + len(onlyAIndex) + len(onlyBIndex)
    elif distFunc == "uem":
        fenzi = 0.5 * sum(bothVal)
        fenmu = 0.5 * sum(bothVal) + len(onlyAIndex) + len(onlyBIndex)   # dist is more, the similarity is stronger
    elif distFunc == "uemnm":
        fenzi = 0.5 * sum(bothVal)
        fenmu = 0.5 * sum(bothVal) + 2 * len(onlyAIndex) + 2 * len(onlyBIndex) + len(bothIndex) + len(bothNotIndex)

    if not IsEqual(fenmu, 0):
        return fenzi / float(fenmu)
    else:
        return 0


#generate SimM listlist
def CalSimM(fv, distFunc):
    N = len(fv) #class count
    simM = list()

    #initialize simM
    for index in range(0, N):
        tmpList = [0] * N #generat a list whole len = N
        simM.append(tmpList)

    for i in range(0, N):
        for j in range(0, N):
            simM[i][j] = CalDistClassij(i, j, fv[i], fv[j], distFunc, thr = 0.01)

    return simM


#python pro.py   concern  distFunc = jm, uem, uemn  
if __name__ == "__main__": 
    fileName = sys.argv[1]
    distFunc = sys.argv[2]

    # read feature vector of each class
    concernFv =ReadCSV(fileName)
    #delete the first column(className) and normalize the fv
    cfv = DelAndNormalize(concernFv)
    #compute all class's pairs 's distunc. The 
    simM = CalSimM(cfv, distFunc)
    
    outFileName = 'jpetstore6_semantic_deps.csv'
    WriteCSV(outFileName, simM)


 
