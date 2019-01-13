import csv
import msconfig

'''
load data from function atom files, calldep files, concerndep files.

generate global allAtoms,  classDepDict


interface:
    loadData()
'''

#dep between class
class DepElement:
    def __init__(self, calldep, concerndep):
        self.calldep = calldep
        self.concerndep = concerndep


class AtomObject:
    def __init__(self, atomId, classIdSet):
        self.atomId = atomId
        self.classIdSet = classIdSet

#output:
#classIDNameDict
#classNameIDDict
#allAtoms = list()   index = id
def loadAtomData(filename):
    classIDNameDict = dict()
    classNameIDDict = dict()
    allAtoms = list()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp)
        atomId = -1
        eleList = list()
        for each in reader:
            [classid,classname,groupId,trace,grouptrace] = each
            if classid == "classid":
                continue
            classid = int(classid)
            classNameIDDict[classname] = classid
            classIDNameDict[classid] = classname

            groupId = int(groupId)
            if groupId != atomId and atomId != -1:
                atomObject = AtomObject(atomId, set(eleList))
                allAtoms.append(atomObject)
            if groupId != atomId:
                eleList = list()
            eleList.append(classid)
            atomId = groupId
            #end for
        atomObject = AtomObject(atomId, set(eleList))
        allAtoms.append(atomObject)
    return classIDNameDict, classNameIDDict, allAtoms




def readCSV(filename):
    listList = list()
    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            listList.append(each)
    return listList


def getDict(depList):
    ClassName2IDDict = msconfig.get_classnameid_dict()
    #print(ClassName2IDDict)
    classDepDict = dict()
    for [class1, class2, dep] in depList:
        if class1 not in ClassName2IDDict or class2 not in ClassName2IDDict:
            continue
        classId1 = ClassName2IDDict[class1]
        classId2 = ClassName2IDDict[class2]
        if classId1 not in classDepDict:
            classDepDict[classId1] = dict()
        if classId2 not in classDepDict[classId1]:
            classDepDict[classId1][classId2] = float(dep)
    return classDepDict


#calldep = c1->c2 + c2->c1
def getCallDep(class1, class2, depDict):
    dep  = 0
    if class1 in depDict and class2 in depDict[class1]:
        dep += depDict[class1][class2]
    if class2 in depDict and class1 in depDict[class2]:
        dep += depDict[class2][class1]
    return dep

#concernDep = c1->c2   or   c2->c1
def getConcernDep(class1, class2, depDict):
    if class1 in depDict and class2 in depDict[class1]:
        return depDict[class1][class2]
    if class2 in depDict and class1 in depDict[class2]:
        return depDict[class2][class1]
    return 0


#generate all deps between all classes based on above loaded deps.
def genFinalDep(classIdList, calldepDict, concernDepDict):
    classDepDict = dict()  #dict[class1][class2] = DepElement(calldep, concerndep)
    for index1 in range(0, len(classIdList)):
        class1 = classIdList[index1]
        if class1 not in classDepDict:
            classDepDict[class1] = dict()
        for index2 in range(0, len(classIdList)):
            class2 = classIdList[index2]
            if class1 != class2:
                callvalue = getCallDep(class1, class2, calldepDict)
                concernValue = getConcernDep(class1, class2, concernDepDict)
                classDepDict[class1][class2] = DepElement(callvalue, concernValue)
    return classDepDict


'''
#classdep= DepElement(calldep, concerndep)
def loadAtomData(atomfileName):
    #load and store atoms.
    #[classIDNameDict, classNameIDDict, allAtoms] = readAtomFile(atomfileName)
    #cannot store into config.
    #msconfig.set_allatom_list(allAtoms)
    #msconfig.set_classidname_dict(classIDNameDict)
    #msconfig.set_classnameid_dict(classNameIDDict)
    return classIDNameDict, classNameIDDict, allAtoms
'''

#compute class-class dep for double - directed. c1->c2= c2->c1
#generate global allAtoms,  classDepDict
def loadDepData(calldepFile, concerndepFile):
    classNameIDDict = msconfig.get_classnameid_dict()
    classIDNameDict = msconfig.get_classidname_dict()
    #print(classNameIDDict, classNameIDDict)
    #load different dep
    calldepList = readCSV(calldepFile)
    concerndepList = readCSV(concerndepFile)
    calldepDict = getDict(calldepList)
    concernDepDict = getDict(concerndepList)

    #generate final deps between all classes based on above loaded deps.
    classIdList = list(classIDNameDict.keys())
    classDepDict = genFinalDep(classIdList, calldepDict, concernDepDict)
    #print("final:")
    #for each1 in classDepDict:
    #    for each2 in classDepDict[each1]:
    #        print(classDepDict[each1][each2].calldep,classDepDict[each1][each2].concerndep )

    #store the data into gloabal config variable.
    return classDepDict



def test():
    #test
    import sys
    atomfileName = sys.argv[1]
    calldepFile = sys.argv[2]
    concerndepFile = sys.argv[3]
    #load and store atoms.
    [classIDNameDict, classNameIDDict, allAtoms] = readAtomFile(atomfileName)
    msconfig.set_allatom_list(allAtoms)
    msconfig.set_classidname_dict(classIDNameDict)
    msconfig.set_classnameid_dict(classNameIDDict)

    #print("classIDNameDict", classIDNameDict)
    #print("classNameIDDict", classNameIDDict)
    #print("atoms:")
    #for atom in allAtoms:
    #    print(atom.atomId, atom.classIdSet)

    #load different dep
    calldepList = readCSV(calldepFile)
    concerndepList = readCSV(concerndepFile)
    calldepDict = getDict(calldepList, classNameIDDict)
    concernDepDict = getDict(concerndepList, classNameIDDict)
    #print("call:", calldepDict)
    #print("concern:", concernDepDict)

    #generate final deps between all classes based on above loaded deps.
    classIdList = list(classIDNameDict.keys())
    classDepDict = genFinalDep(classIdList, calldepDict, concernDepDict)
    #print("final:")
    #for each1 in classDepDict:
    #    for each2 in classDepDict[each1]:
    #        print(classDepDict[each1][each2].calldep,classDepDict[each1][each2].concerndep )

    #store the data into gloabal config variable.
    msconfig.set_classfinaldep_dict(classDepDict)

    #print(msconfig.GLOBAL_VAR_OBJECT.ALLATOM_List)
    #print(msconfig.GLOBAL_VAR_OBJECT.CLASSNAMEIDDict)
    #print(msconfig.GLOBAL_VAR_OBJECT.CLASSIDNAMEDict)
    #print(msconfig.GLOBAL_VAR_OBJECT.CLASSFINALDEPDict)
