import sys
import csv
import understand

'''
before this file, we should use cmtparser.py to parse class-clas cochange

if above generate file-file cochange since the class name->filename is not easy mapping.
thus, in this file:
    we map filename->class2;class1
    commit file-file cochange into class-class cochange.
'''

Global_Class2FileDict = dict() #class (key) read from statis analysis without testclasses
Global_File2ClassesDict = dict()# the result after trans() , [filename] = ["class1, class2,..."]

def readClassFromStatisc(filename):
    f = open(filename, "r")
    for line in f:
        className = line.strip("\n")
        if className not in Global_Class2FileDict:
            Global_Class2FileDict[className] = "0"
    f.close()
    #print(Global_Class2FileDict)

def mapfromund(undname, understand_filename_prefix):
    #open database
    db = understand.open(undname)
    for fileEnt in db.ents("file ~unresolved ~unknown"):
        filename = fileEnt.longname()
        if filename.startswith(understand_filename_prefix):
            filename = filename.split(understand_filename_prefix + "\\")[1] #windows und
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

    print("the class count in static-udb", len(Global_Class2FileDict))

#one file may map into more than one class
def trans():
    for classname in Global_Class2FileDict:
        filename = Global_Class2FileDict[classname]
        if filename not in Global_File2ClassesDict:
            Global_File2ClassesDict[filename] = list()
        Global_File2ClassesDict[filename].append(classname)
    print("the file count in file-classes map:", len(Global_File2ClassesDict))   #one file may includes more than one class


def writeList2File(listlist, filename):
    with open(filename, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(listlist)

#read file-file commit file(cmt-file.csv)
def readCommitFile(filename):
    cochangeAtFileList = list()
    with open(filename, 'r', newline='') as fp:
        reader = csv.reader(fp)
        for each in reader:
            [filename1, filename2, cochange] = each
            cochangeAtFileList.append([filename1, filename2, cochange])
    return cochangeAtFileList


#change cochangeAtFileList into cochangeAtClassList, using Global_File2ClassesDict
def changeAsClass(cochangeAtFileList):
    cochangeAtClassList = list()
    for each in cochangeAtFileList:
        [file1, file2, cochange] = each
        if file1 in Global_File2ClassesDict and file2 in Global_File2ClassesDict:
            classList1 = Global_File2ClassesDict[file1]
            classList2 = Global_File2ClassesDict[file2]
            for class1 in classList1:
                for class2 in classList2:
                    tmp = [class1, class2, cochange]
                    cochangeAtClassList.append(tmp)
    return cochangeAtClassList

'''
python ../../../split/classstatis/cmtfilenameMap2ClassName.py  xwiki-platform108_all_class.txt  ../dependency/xw
iki-platform108.udb   cmt-file.csv cmt-class.csv
'''
if __name__ =="__main__":

    staticClassFilename = sys.argv[1]
    understandFilename  = sys.argv[2]
    #understand_filename_prefix = sys.argv[3]  #C:\xwiki-platform
    commit_file2file_filename = sys.argv[3]
    commit_class2class_filename = sys.argv[4]  #output

    #read key=clasname from .und  into Global_Class2FileDict
    readClassFromStatisc(staticClassFilename)
    #read value=file into Global_Class2FileDict[classname], that is, map from classname to filename
    mapfromund(understandFilename, r'C:\xwiki-platform')

    #class2filed to file2classes, output Global_File2ClassesDict
    trans()

    #read file-file commit file(cmt-file.csv)
    cochangeAtFileList = readCommitFile(commit_file2file_filename)

    #change cochangeAtFileDict into cochangeAtClassList, using Global_File2ClassesDict
    cochangeAtClassList = changeAsClass(cochangeAtFileList)
    writeList2File(cochangeAtClassList, commit_class2class_filename)
