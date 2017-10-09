'''
use all the enum option as popilation, do the preto analysis
'''
import fastnondomsort
import config
import fitness
import initpop

FITNESSFILENAME  = config.GlobalVar.FITNESSFILENAME
BIT_COUNT_X = config.GlobalVar.BIT_COUNT_X
BIT_COUNT_Y = config.GlobalVar.BIT_COUNT_Y

if __name__ == '__main__':

    #load all fitness value
    fitness.loadFitness(FITNESSFILENAME) #set OBJECT_STRUCT_DICT
    OBJECT_STRUCT_DICT = config.get_object_struct()
    for serv in OBJECT_STRUCT_DICT:
        for thr_int in OBJECT_STRUCT_DICT[serv]:
            one = OBJECT_STRUCT_DICT[serv][thr_int]
            print serv, thr_int, one.nonlapClassCount, one.nonlapClassCount_avg, one.withinWorkflow, one.interWorklow, one.APINum, one.APINum_avg
    print 'loadFitness finished....\n'

    #add all indivs into pop_list
    pop_list = list()#[i] = indiv
    real_dict = dict() #[indiv] = [xi, yi]
    for serv in OBJECT_STRUCT_DICT:
        for thr_int in OBJECT_STRUCT_DICT[serv]:
            if serv >= 2 and serv <= 3  and thr_int >= 10 and thr_int <= 50:
                xi = serv
                yi = thr_int
                xibit = initpop.Dec2bit(xi, BIT_COUNT_X)
                yibit = initpop.Dec2bit(yi, BIT_COUNT_Y)
                indiv = xibit + yibit
                real_dict[indiv] = [xi, yi]
                pop_list.append(indiv)

    # fast non dominate sort
    [layerList, indivRankDict] = fastnondomsort.FastNondomSort(pop_list)
    print 'pop= ', len(pop_list)
    print 'layer= ', len(layerList)
    for listlist in layerList:
        print len(listlist)
    for indiv in layerList[0]:
        print real_dict[indiv]
