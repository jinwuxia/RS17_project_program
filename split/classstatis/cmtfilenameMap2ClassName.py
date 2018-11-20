import sys
import csv
import understand

staticClassFilename = sys.argv[1]
understandFilename  = sys.argv[2]
cmtfilelistFilename = sys.argv[3]
understand_filename_prefix = sys.argv[4]  #C:\xwiki-platform
mapfilename = sys.argv[5]

Global_Class2FileDict = dict() #class (key) read from statis analysis without testclasses
Global_File2ClassesDict = dict()  #[filename] = []"class1, class2,..."]

def readClassFromStatisc(filename):
    f = open(filename, "r")
    for line in f:
        className = line.strip("\n")
        if className not in Global_Class2FileDict:
            Global_Class2FileDict[className] = "0"
    f.close()
    #print(Global_Class2FileDict)

def mapfromund(undname):
    #open database
    db = understand.open(undname)
    for fileEnt in db.ents("file ~unresolved ~unknown"):
        filename = fileEnt.longname()
        if filename.startswith(understand_filename_prefix):
            filename = filename.split(understand_filename_prefix + "\\")[1]
        else:
            #print("abnormal: " , filename)
            continue

        #print("filename in und: ", filename)
        if "\\" in filename:
            arr = filename.split("\\")
            filename = "/".join(arr)
        #print("filename new   : ", filename)

        ents = list()
        ents.extend(fileEnt.ents("Define", "class ~unresolved ~unknown"))
        ents.extend(fileEnt.ents("Define", "interface ~unresolved ~unknown"))
        #print(len(ents))
        for classEnt in ents:
            className = classEnt.longname()
            if className in Global_Class2FileDict:
                Global_Class2FileDict[className] = filename
                #print (className, filename)
            else:
                #print("not: ", className)
                pass

    print("the class count ", len(Global_Class2FileDict))

def trans():
    for classname in Global_Class2FileDict:
        filename = Global_Class2FileDict[classname]
        if filename not in Global_File2ClassesDict:
            Global_File2ClassesDict[filename] = list()
        Global_File2ClassesDict[filename].append(classname)
    print("the file count which contains above classes:", len(Global_File2ClassesDict))   #one file may includes more than one class

#Global_File2ClassesDict to file
def writeTrans2File(listlist):
    with open(mapfilename, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)

#export [cmt_file_nanme= und_file_name, classnamelist]
def filterCmtfilelist(cmtfilename):
    listlist= list()
    matchedFileCount = 0
    with open(cmtfilename, "r", newline="") as fp:
        reader = csv.reader(fp)
        for each in reader:
            cmtname = each[0]
            if cmtname in Global_File2ClassesDict:
                matchedFileCount += 1
                listlist.append([ cmtname, ";".join(Global_File2ClassesDict[cmtname]) ])
    print ("the number of file in commit matched with project nontest file: ", matchedFileCount)
    return listlist

#dict[classID1][classID2] = commit_times_together
def change2Pair(listList):
    commitDict = dict()
    for eachList in listList:
        from itertools import permutations
        tmp = list(permutations(eachList, 2))
        for each in tmp:
            [id1, id2] = each
            if id1 not in commitDict:
                commitDict[id1] = dict()
            if id2 not in commitDict[id1]:
                commitDict[id1][id2] = 1
            else:
                commitDict[id1][id2] += 1

    return commitDict

r"""
python ../../../split/classstatis/cmtfilenameMap2ClassName.py  xwiki-platform108_all_class.txt  ../dependency/xw
iki-platform108.udb   ../dependency/xwiki-platform-commit-filenames.csv  "C:\xwiki-platform"  xwiki-platform-class-file-map.csv
"""
def main():
    readClassFromStatisc(staticClassFilename) #read key in Global_Class2FileDict
    mapfromund(understandFilename) #read value in Global_Class2FileDict
    #class2filed to file2classes
    trans()

    listlist = filterCmtfilelist(cmtfilelistFilename) #match and summary the number of macthed files

    writeTrans2File(listlist)



main()
