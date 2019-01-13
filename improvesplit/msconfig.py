'''
data explain:
indiv=[candidate, candidate, ..]
candidate=[atom1, atom2, ...]
atom = atomobject(atomid, set of classids)
'''


class GLOBAL_VAR_OBJECT:
    ALLATOM_List = list()  #[i]= AtomObject. i = atomId
    CLASSNAMEIDDict = dict()
    CLASSIDNAMEDict = dict()
    CLASSFINALDEPDict = dict()

    #the parameter of the algorithm
    POP_SIZE = 40
    PARTITION_K = 10
    PARENT_M = 14
    FITNESS_METHOD_LIST = ["call coh without weight","call coup without weight","concern coh without weight","concern coup without weight"]
    CROSSOVER_OPERATOR = "1PNC"
    MUTATION_PROBABILITY = 0.2  #0.01-0.2
    MUTATION_OPERATOR = "random"
    MAX_ITERATION_LOOP = 100
    CONTINUE_BEST_LOOP  = 50
    REPEAT_TIMES = 1
    CURRENT_CONTINUE_BEST_LOOP = 0
    current_knee_point = list()

    all_candidate_call_coh_dict = dict()
    all_candidate_call_coup_dict = dict()
    all_candidate_con_coh_dict = dict()
    all_candidate_con_coup_dict = dict()

def set_allatom_list(atomlist):
    GLOBAL_VAR_OBJECT.ALLATOM_List = atomlist

def get_allatom_list():
    return GLOBAL_VAR_OBJECT.ALLATOM_List

def set_classnameid_dict(adict):
    GLOBAL_VAR_OBJECT.CLASSNAMEIDDict = adict

def get_classnameid_dict():
    return GLOBAL_VAR_OBJECT.CLASSNAMEIDDict

def set_classidname_dict(adict):
    GLOBAL_VAR_OBJECT.CLASSIDNAMEDict = adict

def get_classidname_dict():
    return GLOBAL_VAR_OBJECT.CLASSIDNAMEDict

def set_classfinaldep_dict(adict):
    GLOBAL_VAR_OBJECT.CLASSFINALDEPDict = adict

def get_classfinaldep_dict():
    return GLOBAL_VAR_OBJECT.CLASSFINALDEPDict

def add_continue_best_loop():
    GLOBAL_VAR_OBJECT.CURRENT_CONTINUE_BEST_LOOP += 1  #crrrent + 1

def reset_continue_best_loop():
    GLOBAL_VAR_OBJECT.CURRENT_CONTINUE_BEST_LOOP = 0 #reset current = 0

def get_continue_best_loop():
    return GLOBAL_VAR_OBJECT.CURRENT_CONTINUE_BEST_LOOP


def set_all_candidate_call_coh_dict(all_candidate_call_coh_dict):
    GLOBAL_VAR_OBJECT.all_candidate_call_coh_dict = all_candidate_call_coh_dict

def set_all_candidate_call_coup_dict(all_candidate_call_coup_dict):
    GLOBAL_VAR_OBJECT.all_candidate_call_coup_dict = all_candidate_call_coup_dict

def set_all_candidate_con_coh_dict(all_candidate_con_coh_dict):
    GLOBAL_VAR_OBJECT.all_candidate_con_coh_dict = all_candidate_con_coh_dict

def set_all_candidate_con_coup_dict(all_candidate_con_coup_dict):
    GLOBAL_VAR_OBJECT.all_candidate_con_coup_dict = all_candidate_con_coup_dict

def get_all_candidate_call_coh_dict():
    return GLOBAL_VAR_OBJECT.all_candidate_call_coh_dict

def get_all_candidate_call_coup_dict():
    return GLOBAL_VAR_OBJECT.all_candidate_call_coup_dict

def get_all_candidate_con_coh_dict():
    return GLOBAL_VAR_OBJECT.all_candidate_con_coh_dict

def get_all_candidate_con_coup_dict():
    return GLOBAL_VAR_OBJECT.all_candidate_con_coup_dict

def get_current_knee_point():
    return GLOBAL_VAR_OBJECT.current_knee_point

def set_current_knee_point(current_knee_point):
    GLOBAL_VAR_OBJECT.current_knee_point = current_knee_point
