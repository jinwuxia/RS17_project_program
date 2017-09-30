class GlobalVar:
    #step1: init population
    N = 14 #initial populization size, each generation size = intialSize
    M = 8 #silect base
    K = 6 #elict parents
    #for jpetstore6
    X_S = 2
    X_E = 10
    BIT_COUNT_X = 4
    BIT_COUNT_Y = 7
    FITNESSFILENAME = '../../../testcase_data/jpetstore6/coreprocess/jpetstore6-fitness.csv'
    '''
    #for jforum219_1
    X_S = 18
    X_E = 47
    BIT_COUNT_X = 6
    BIT_COUNT_Y = 7
    FITNESSFILENAME = '../../../testcase_data/jforum219_1/coreprocess/jforum219-fitness.csv'
    '''
    Y_S = 1
    Y_E = 100

    OBJECT_STRUCT_DICT = dict()
    FITNESS_METHOD = 'withinwf-interwf-repclass'  #or withinwf or withinwf-interwf-repclass
    FITNESS_METHOD_LIST = ['withinwf', 'repclassnum', 'clusternum']
    SELECTED_METHOD = 'SA'  #PRO or SA
    FITNESS_PROBABILITY = 0.10
    TEM = 10000
    COOLING_RATE = 0.98

    MAX_ITERATION_LOOP = 10000
    CONTINUE_BEST_LOOP  = 100
    CURRENT_CONTINUE_BEST_LOOP = 0

    CROSS_OPERATOR = '2P2C'
    #CHILDREN_NUM = 4

    MUTATION_PROBABILITY = 0.02
    MUTATION_OPERATOR = 'worse' #random  or worse

def set_object_struct(oneDict):
    GlobalVar.OBJECT_STRUCT_DICT = oneDict

def get_object_struct():
    return GlobalVar.OBJECT_STRUCT_DICT



def add_continue_best_loop():
    GlobalVar.CURRENT_CONTINUE_BEST_LOOP += 1  #crrrent + 1

def reset_continue_best_loop():
    GlobalVar.CURRENT_CONTINUE_BEST_LOOP = 0 #reset current = 0

def get_continue_best_loop():
    return GlobalVar.CURRENT_CONTINUE_BEST_LOOP
