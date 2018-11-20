import sys
import csv
import math
import re


Word_idf_dict = dict()  #dict[word] = idf
Doc_word_tfidf_dict = dict() #dict[docName][word] = tf-idf value
Doc_word_freq_dict = dict() #dict[docName][word] = freq  #word 's appearing times in docName file'
Word_doc_dict = dict()  #dict[word] = [doc1, doc2,....]   word's documen list
Keyword_set = set()  # by using td-idf
Java_stop_words = ['public', 'private','protected','static', 'null', 'class', 'system','out', 'in', 'print', 'println', 'debug',\
                    'int','string', 'this', 'return', 'double', 'throw', 'exception', 'void', 'try', 'catch', 'final', 'main', \
                    'vector', 'execute', 'long', 'if', 'else', 'continue', 'break', 'while', 'do', 'for','size', 'is', 'new', \
                    'null', 'package', 'import', 'hashmap', 'integer', 'decimal', 'get', 'set', 'boolean','first', 'byte', 'char',\
                    'org', 'mybatis', 'jpetstore', 'domain', 'mapper', 'action', 'action', 'web', 'bean', 'service', 'abstract',\
                    'list', 'map', 'lang', 'type', 'add','sub', 'next', \
                    'net', 'jforum', 'is','dao','entities', 'util','api', 'cache', 'context', 'exception', 'search', 'repository', 'admin', 'legacy',\
                    'weblogger', 'pojo', 'business', 'util', 'planet', 'roller', 'apache', 'org', 'core', 'config', 'rendering', 'ajax', 'admin', 'editor',\
                    'tag', 'webservice', 'model', 'repository', 'service', 'controller',\
		            'api', 'cache', 'event', 'dev', 'model', 'filter', 'processor', 'util',\
                    'xwiki', 'wiki', "misc","flavor","storage","escaping","selenium","ui","webstandards","activeinstalls","admin","annotations","extension",\
                    "filter","flamingo", "skin","theme","index","linkchecker","mail","menu","messagestream","notification","observation","office","panel",\
                    "release","repository","resource","rest","scheduler","sharepage","user","directory","profile","vfs","watchlist","webjars","wiki","xclass"]



# split by hump
def splitByHump(name):
    resList = list()
    upperIndexList = list()
    upperIndexList.append(0) #first index
    for index in range(0, len(name)):
        if name[index].isupper():
            upperIndexList.append(index)
    upperIndexList.append(len(name)) #last index + 1

    for i in range(0, len(upperIndexList) - 1):
        index_s = upperIndexList[i]
        index_e = upperIndexList[i + 1]
        strstr = name[index_s: index_e]
        resList.append(strstr)

    resList = [each.lower() for each in resList]
    return resList


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
        if docName not in Word_doc_dict[word]:
            Word_doc_dict[word].append(docName)

#filter by 's/d' or 'ing ' or 'number' endsup
def removeNumFushu(word):
    if word.endswith('s') and word.endswith('es') == False:
        word = word[0: len(word) - 1]

    elif len(word) > 2 and (word.endswith('ed') or word.endswith('es')):
        word = word[0: len(word) - 2]
        if len(word) > 2 and word[len(word) -1 ] == word[len(word) - 2]:
            word = word[0: len(word) - 1]

    elif word.endswith('ing'):
        word = word[0: len(word) - 3]
        if len(word) > 2 and word[len(word) -1 ] == word[len(word) - 2]:
            word = word[0: len(word) - 1]

    if re.search(r'[0-9]+', word):
        #print word
        m = re.search(r'[0-9]+', word)  #search any-pos substring,  match from start
        #print 'match:', m.group() #match's str
        (start, end) = m.span() #match pos
        if start < end:
            word = ( word[0: start] + word[start + 1: end] + word[end + 1 : len(word)] )
        elif start == end:
            word = ( word[0: start] + word[start + 1: len(word)] )
        #print word
    return word

def isAllBigLetter(word):
    if re.match(r'[A-Z_0-9]+', word):  #all big letter
        m = re.match(r'[A-Z_0-9]+', word)
        if len(m.group()) == len(word):
            return True
    return False


def processIdentifierFile(fileName):
    #stopWords
    import nltk
    nltk.download('stopwords')
    stopWords = nltk.corpus.stopwords.words('english')
    stopWords.extend(Java_stop_words)

    with open (fileName, 'r') as fp:
        for line in fp.readlines(): #eachline corresponds to a class
            line = line.strip()
            tmpList = line.split(',')
            className = tmpList[0]
            rawwordList = tmpList[1:len(tmpList)]

            #if words are all captain letter
            for i in range(0, len(rawwordList)):
                if isAllBigLetter(rawwordList[i]):
                    rawwordList[i] = rawwordList[i].lower()

            #split by . or  _
            wordList = list()
            for word in rawwordList:
                tmpList = re.split( r'[._\[\]]', word)
                #print 'raw: ', word
                #print 'split by ._:', ','.join(tmpList)
                wordList.extend(tmpList)

            #split by hump
            newWordList = list()
            for word in wordList:
                tmpList = splitByHump(word)
                #print 'raw: ', word
                #print 'split by hump:', ','.join(tmpList)
                newWordList.extend(tmpList)

            #filter
            wordList = list()
            for word in newWordList:
                word = removeNumFushu(word) #filter by 's' or 'number' endsup
                if (word != '') and (len(word) > 2) and (word not in stopWords):
                    wordList.append(word)

            #print className, ':'
            #print ','.join(wordList)
            #print "\n"
            if len(wordList) != 0:
                 firstPass(className, wordList)
            else:
                 print(className, "wordList = 0")
    fp.close()


#Word_idf_dict
def computeIDF():
    #docCOunt
    docCount = len(Doc_word_freq_dict)
    for word in Word_doc_dict:
        value = math.log( docCount/ float(len(Word_doc_dict[word]) + 1) )
        Word_idf_dict[word] = value


#for all document, extract its keyword
#generate Doc_word_tfidf_dict
#reutn keywords=list
def extractKeyWord(THR):
    for docName in Doc_word_freq_dict:
        Doc_word_tfidf_dict[docName] = dict()
        #print(docName,Doc_word_freq_dict[docName])
        max_freq = max( Doc_word_freq_dict[docName].values() )
        for word in Doc_word_freq_dict[docName]:
            tf = Doc_word_freq_dict[docName][word] / float(max_freq)
            idf = Word_idf_dict[word]
            tfidf = tf * idf
            Doc_word_tfidf_dict[docName][word] = tfidf

        #get first THR number of word as keywords
        sortedDict = sorted(Doc_word_tfidf_dict[docName].items(), key=lambda x:x[1], reverse=True)

        counter = 0
        for (key, value) in sortedDict:
            if counter < int(1 + THR * len(Doc_word_tfidf_dict[docName]) ):
                Keyword_set.add(key)
                counter += 1
            else:
                break

#according keywordlist, generate feature vector list
def genVector():
    vectorList = list() #list[0]= [docname, f1,f2,...]
    keywordList = list(Keyword_set)
    for docName in Doc_word_freq_dict:
        tmp = list()
        tmp.append(docName)
        for word in keywordList:
            if word in Doc_word_freq_dict[docName]:
                freq = Doc_word_freq_dict[docName][word]
            else:
                freq = 0
            tmp.append(freq)
        vectorList.append(tmp)
    return vectorList

def writeCSV(listList, fileName):
    with open(fileName, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print (fileName)


#python pro.py  jpetstore6_words.txt  fvname thr=0.9
if __name__ == '__main__':
    wordFileName = sys.argv[1]
    fvFileName = sys.argv[2]
    #thr = float(sys.argv[3])
    processIdentifierFile(wordFileName)
    '''
    print "\n"
    for docName in Doc_word_freq_dict:
        print 'clasName: ', docName
        print 'dict:', Doc_word_freq_dict[docName]
    print "\n"
    for word in Word_doc_dict:
        print 'word: ', word
        print 'doc_list:', Word_doc_dict[word]
    '''
    print ('doc  count: ', len(Doc_word_freq_dict))
    print ('word count: ', len(Word_doc_dict))

    #compute tf-idf, sort and generate keywordList
    computeIDF()
    extractKeyWord(0.5) #60% word in each doc are as keywords
    print ('total keyword: ', Keyword_set)
    print ('keyword count: ', len(Keyword_set))
    fvList = genVector()
    writeCSV(fvList, fvFileName)
