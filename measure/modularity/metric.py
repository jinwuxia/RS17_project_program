import csv
import config

'''
interface:
getFitnessForPopulation(population, fitness_method)
getFitness(fitnessMethod, indiv)
get_four_metrics(indiv)
'''
# aservice candidate = the list of classIds
def getClasssetForCandidate(candidate):
    classset = set(candidate)
    return classset


#candidate = list of atomIds
#input[4,2,3]
#ouput(2,3,4)
def uniqueEncode(candidate):
    candidate.sort()
    candidate = tuple(candidate)
    return candidate

#inside connections / n*(n-1),  intra-connections in bunch paper.
def computeCallcohForCandidate(candidate):
    CLASSFINALDEPDict = config.get_classfinaldep_dict()
    classset = getClasssetForCandidate(candidate)
    allconnections = len(classset) * len(classset)
    hasconnections = 0
    for class1 in classset:
        for class2 in classset:
            if class1 != class2 and int(CLASSFINALDEPDict[class1][class2].calldep)!=0:
                hasconnections += 1
    value = hasconnections / float (allconnections) #one candidate's cohesion
    return value


def computeCallcoupForCandidate(candidate1, candidate2):
    CLASSFINALDEPDict = config.get_classfinaldep_dict()
    set1 = getClasssetForCandidate(candidate1)
    set2 = getClasssetForCandidate(candidate2)
    #compute the coupling between set1 and set2
    connections = 0
    maximumConnections = len(set1) * len(set2)
    for class1 in set1:
        for class2 in set2:
            if int(CLASSFINALDEPDict[class1][class2].calldep) != 0:
                connections += 1
    value = connections / float(maximumConnections)
    return value


def computeConcohForCandidate(candidate):
    CLASSFINALDEPDict = config.get_classfinaldep_dict()
    #transform candidate={atom} to a class set
    classset = getClasssetForCandidate(candidate)
    allconnections = len(classset) * len(classset)
    hasconnections = 0
    for class1 in classset:
        for class2 in classset:
            if class1 != class2 and CLASSFINALDEPDict[class1][class2].concerndep >= 0.2000:
                hasconnections += 1
    value = hasconnections / float (allconnections) #one candidate's cohesion
    return value


def computeConcoupForCandidate(candidate1, candidate2):
    CLASSFINALDEPDict = config.get_classfinaldep_dict()
    set1 = getClasssetForCandidate(candidate1)
    set2 = getClasssetForCandidate(candidate2)
    #compute the coupling between set1 and set2
    connections = 0
    maximumConnections = len(set1) * len(set2)
    for class1 in set1:
        for class2 in set2:
            if CLASSFINALDEPDict[class1][class2].concerndep >= 0.2000:
                connections += 1
    value =  connections / float(maximumConnections)
    return value


#[candidate]=
def computeFitnessThread_callcoh(pop_list):
    candidateMetricDict = dict()
    for indiv in pop_list:
        for candidate in indiv:
            uniqueCandidate = uniqueEncode(candidate)
            if uniqueCandidate not in candidateMetricDict:
                candidateMetricDict[uniqueCandidate] = computeCallcohForCandidate(candidate)
    return candidateMetricDict


#return [candidate1][candidate2]= metric
def computeFitnessThread_callcoup(pop_list):
    candidateMetricDict = dict()
    for indiv in pop_list:
        candidateList = indiv
        for candidate1 in candidateList:
            uni_candidate1 = uniqueEncode(candidate1)
            if uni_candidate1 not in candidateMetricDict:
                candidateMetricDict[uni_candidate1] = dict()
            for candidate2 in candidateList:
                uni_candidate2 = uniqueEncode(candidate2)
                if candidate1 != candidate2 and uni_candidate2 not in candidateMetricDict[uni_candidate1]:
                    candidateMetricDict[uni_candidate1][uni_candidate2] = computeCallcoupForCandidate(candidate1, candidate2)
                    if uni_candidate2 not in candidateMetricDict:
                        candidateMetricDict[uni_candidate2] = dict()
                    candidateMetricDict[uni_candidate2][uni_candidate1] = candidateMetricDict[uni_candidate1][uni_candidate2]

    return candidateMetricDict


#[canidate]=
def computeFitnessThread_concoh(pop_list):
    candidateMetricDict = dict()
    for indiv in pop_list:
        for candidate in indiv:
            uniqueCandidate = uniqueEncode(candidate)
            if uniqueCandidate not in candidateMetricDict:
                candidateMetricDict[uniqueCandidate] = computeConcohForCandidate(candidate)
    return candidateMetricDict

#return [candidate1][candidate2]= metric
def computeFitnessThread_concoup(pop_list):
    candidateMetricDict = dict()
    for indiv in pop_list:
        candidateList = indiv
        for candidate1 in candidateList:
            uni_candidate1 = uniqueEncode(candidate1)
            if uni_candidate1 not in candidateMetricDict:
                candidateMetricDict[uni_candidate1] = dict()
            for candidate2 in candidateList:
                uni_candidate2 = uniqueEncode(candidate2)
                if candidate1 != candidate2 and uni_candidate2 not in candidateMetricDict[uni_candidate1]:
                    candidateMetricDict[uni_candidate1][uni_candidate2] = computeConcoupForCandidate(candidate1, candidate2)
    return candidateMetricDict


#interfacce
#compute metrics for candidate
def computeFitnessThread(pop_list, fitness_method_list):
    for fitnessMethod in fitness_method_list:
        if fitnessMethod == "call coh without weight":
            all_candidate_call_coh_dict = computeFitnessThread_callcoh(pop_list)
            #store
            config.set_all_candidate_call_coh_dict(all_candidate_call_coh_dict)

        elif fitnessMethod == "call coup without weight":
            all_candidate_call_coup_dict = computeFitnessThread_callcoup(pop_list)
            #store
            config.set_all_candidate_call_coup_dict(all_candidate_call_coup_dict)

        elif fitnessMethod == "concern coh without weight":
            all_candidate_con_coh_dict = computeFitnessThread_concoh(pop_list)
            #store
            config.set_all_candidate_con_coh_dict(all_candidate_con_coh_dict)

        elif fitnessMethod == "concern coup without weight":
            all_candidate_con_coup_dict = computeFitnessThread_concoup(pop_list)
            #store
            config.set_all_candidate_con_coup_dict(all_candidate_con_coup_dict)

        else:
            print("Do not support this fitness:", fitnessMethod)


def get_call_coh_ForIndiv(indiv):
    all_candidate_call_coh_dict = config.get_all_candidate_call_coh_dict()
    coh_list = list()
    for candidate in indiv:
        uni_candidate = uniqueEncode(candidate)
        coh = all_candidate_call_coh_dict[uni_candidate]
        coh_list.append(coh)
    indiv_metric = sum(coh_list) / float(len(coh_list))
    return indiv_metric, coh_list


def get_call_coup_ForIndiv(indiv):
    all_candidate_call_coup_dict = config.get_all_candidate_call_coup_dict()
    coup_list = list()
    for index1 in range(0, len(indiv) -1 ):
        cand1 = uniqueEncode(indiv[index1])
        for index2 in range(index1 + 1, len(indiv)):
            cand2 = uniqueEncode(indiv[index2])
            coup = all_candidate_call_coup_dict[cand1][cand2]
            coup_list.append(coup)
    indiv_metric = sum(coup_list) / float(len(coup_list))
    return indiv_metric,coup_list




def get_con_coh_ForIndiv(indiv):
    all_candidate_con_coh_dict = config.get_all_candidate_con_coh_dict()
    coh_list = list()
    for candidate in indiv:
        uni_candidate = uniqueEncode(candidate)
        coh = all_candidate_con_coh_dict[uni_candidate]
        coh_list.append(coh)
    indiv_metric = sum(coh_list) / float(len(coh_list))
    return indiv_metric,coh_list


def get_con_coup_ForIndiv(indiv):
    all_candidate_con_coup_dict = config.get_all_candidate_con_coup_dict()
    coup_list = list()
    for index1 in range(0, len(indiv) -1 ):
        cand1 = uniqueEncode(indiv[index1])
        for index2 in range(index1 + 1, len(indiv)):
            cand2 = uniqueEncode(indiv[index2])
            coup = all_candidate_con_coup_dict[cand1][cand2]
            coup_list.append(coup)
    indiv_metric = sum(coup_list) / float(len(coup_list))
    return indiv_metric,coup_list


def get_four_metrics(indiv):
    [call_coh, call_coh_detail]  = get_call_coh_ForIndiv(indiv)
    [call_coup, call_coup_detail] = get_call_coup_ForIndiv(indiv)
    [con_coh, con_coh_detail] = get_con_coh_ForIndiv(indiv)
    [con_coup, con_coup_detail] = get_con_coup_ForIndiv(indiv)

    #print detail
    print('call coh detail:')
    printList(call_coh_detail)
    print('\ncall coup detail')
    printList(call_coup_detail)
    print('\nsema coh detail')
    printList(con_coh_detail)
    print('\n sema coup detail')
    printList(con_coup_detail)

    return call_coh, call_coup, con_coh, con_coup

def printList(qlist):
    for each in qlist:
        print(each)
