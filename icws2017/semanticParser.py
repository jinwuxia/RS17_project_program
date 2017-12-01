import sys
import csv
import math


Word_idf_dict = dict()  #dict[word] = idf
Doc_word_tfidf_dict = dict() #dict[docName][word] = tf-idf value
Doc_word_freq_dict = dict() #dict[docName][word] = freq  #word 's appearing times in docName file'
Word_doc_dict = dict()  #dict[word] = [doc1, doc2,....]   word's documen list
Keyword_set = set()  # by using td-idf
Java_stop_words = ['public', '']
Punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*', '<', '>']

#modify  Doc_word_freq_dict, Word_doc_dict
def firstPass(docName, wordList):
    Doc_word_freq_dict[docName] = dict()
    for word in wordList:
        if word not in Doc_word_freq_dict[docName]:
            Doc_word_freq_dict[docName][word] = dict()
            Doc_word_freq_dict[docName][word] = 1
        else:
            Doc_word_freq_dict[docName][word] += 1


        if word not in Word_doc_dict:
            Word_doc_dict[word] = list()
        Word_doc_dict[word].append(docName)


#for each ele, split by hump
def SplitHump(oneList):
    resList = list()
    for name in oneList:
        upperIndexList = list()
        upperIndexList.append(0) #first index
        for index in range(0, len(name)):
            if name[index].isupper():
                upperIndexList.append(index)
        upperIndexList.append(index + 1) #last index + 1

        for i in range(0, len(upperIndexList) - 1):
            index_s = upperIndexList[i]
            index_e = upperIndexList[i + 1]
            strstr = name[index_s: index_e]
            resList.append(strstr)
    return resList

#split(., tuofeng) each name to items, and ignore the non-domain item
def GetItems(nameSet):
    itemList = list()
    for name in nameSet:
        #split
        tmpList = re.split( r'[._]', name)
        tmpList = SplitHump(tmpList)
        tmpList = [each.lower() for each in tmpList]
        itemList.extend(tmpList)
    newItemList = list()
    for item in itemList:
        if IsIgnored(item) == False and item != '':
            newItemList.append(item)
    #print 'before=', nameSet
    #print 'after =', set(newItemList)
    return set(newItemList)


def prcessFiles(fileDir):
    #find all the sourcecode file in the directory
    for eachFileName in fileNameList:
        className = getClassName(eachFileName)
        fp = open(eachFileName, 'rb')
        rawdata = read(fp)

        #tokenzie
        wordToken = nltk.tokenize.word_tokenize(rawdata)
        stopWords = nltk.corpus.stopwords.words('english')
        stopWords.extend(Java_stop_words)
        newWordToken = list()
        for word in wordToken:
            if word not in stopWords:
                newWordToken.append(word)

        #remove punctuation and number
        newnewWordToken = list()
        if word in newWordToken:
            if word not in Punctuations:
                newnewWordToken.append(word)

        #change capital letter to lower-case letter
        newnewWordToken = [each.lower() for each in newnewWordToken]

        #tokenize, camel-casing tokenize, '_'tokenize






#Word_idf_dict
def computeIDF():
    #docCOunt
    docCount = len(Doc_word_tfidf_dict)
    for word in Word_doc_dict:
        value = math.log( docCount/ float(len(Word_doc_dict[word]) + 1) )
        Word_idf_dict[word] = value



#for all document, extract its keyword
#generate Doc_word_tfidf_dict
#reutn keywords=list
def extractKeyWord(THR):
    for docName in Doc_word_freq_dict:
        Doc_word_tfidf_dict[docName] = dict()
        max_freq = max(Doc_word_freq_dict[docName].items())
        for word in Doc_word_freq_dict[docName]:
            tf = Doc_word_freq_dict[docName][word] / float(max_freq)
            idf = Word_idf_dict[word]
            tfidf = tf * idf
            Doc_word_tfidf_dict[docName][word] = tfidf

        #get first THR number of word as keywords
        sortedDict = sorted(Doc_word_tfidf_dict[docName].items(), key=lambda x:x[1], reverse=True)
        counter = 0
        for (key, items) in sortedDict:
            if counter < THR:
                Keyword_set.add(key)
                counter += 1
            else:
                break
    print 'total keyword number: ', len(Keyword_set)

#according keywordlist, generate feature vector list
def genVector():
    vectorList = list() #list[0]= [docname, f1,f2,...]
    keywordList = list(Keyword_set)
    for docName in Doc_word_freq_dict:
        tmp = list()
        tmp.append(docName)
        for word in keywordList:
            tmp.append(Doc_word_freq_dict[Doc_word_freq_dict][word])
        vectorList.append(tmp)
    return vectorList

def writeCSV(listList, fileName):
    with open(fileName, 'wb') as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print fileName


if __name__ == '__main__':

    firstPass(docName, wordList)
    computeIDF()
    #compute tf-idf, sort and generate keywordList
    extractKeyWord(each_keyword_number)
    fvList = genVector()
    writeCSV(fvList, fileName)
