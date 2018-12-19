'''
data explain:
indiv=[candidate, candidate, ..]
candidate=[CLASSID1, CLASSID2, ...]
'''


class GLOBAL_VAR_OBJECT:
    FITNESS_METHOD_LIST=["call coh without weight","call coup without weight","concern coh without weight","concern coup without weight"]
    CLASSNAMEIDDict = dict()
    CLASSIDNAMEDict = dict()
    CLASSFINALDEPDict = dict()


    all_candidate_call_coh_dict = dict()
    all_candidate_call_coup_dict = dict()
    all_candidate_con_coh_dict = dict()
    all_candidate_con_coup_dict = dict()


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
