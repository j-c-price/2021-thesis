import glob
import os
import re
import subprocess
from time import sleep
from nltk import ngrams

#import NeuralCRF
#from NeuralCRF import simplification
import numpy as np
import numpy.linalg as LA
import pysrt
import textdistance
from natsort import os_sorted
from sklearn.feature_extraction.text import TfidfVectorizer


# Compare each line of SRT to a whole slide of ppt text
def srtAndSlideTextWordJaccard(srtFilename, SlideArray, n):
    subs = pysrt.open(srtFilename, encoding='iso-8859-1')
    i = 0
    dis = np.zeros((len(subs), len(SlideArray)))
    dis = dis * 1.0
    count = 0
    while (i < len(subs)):
        for j in range(len(SlideArray) - 1):
            #dis[i][j] = textdistance.jaccard.distance(subs[i].text.split(), SlideArray[j].split())
            dis[i][j] = textdistance.jaccard.distance(ngrams(subs[i].text.split(), n), ngrams(SlideArray[j], n))
            j += 1
            count += 1
        i += 1
    max = np.amax(dis, 1)
    i = 0
    result = []
    while (i < len(subs)):
        result.append(np.where(dis[i] == max[i])[0][0])
        i += 1
    return result

def sharedwords(s1,s2):
    res = []
    ls1, ls2 = set(s1.split()), set(s2.split())
    for word in ls1:
        if word in ls2: res.append(word)
    return res

# Compare each line of SRT to a whole slide of ppt text
def srtAndSlideTextWordOverlap(srtFilename, SlideArray):
    subs = pysrt.open(srtFilename, encoding='iso-8859-1')
    i = 0
    dis = np.zeros((len(subs), len(SlideArray)))
    dis = dis * 1.0
    count = 0
    while (i < len(subs)):
        for j in range(len(SlideArray) - 1):
            dupli = sharedwords(subs[i].text, SlideArray[j])
            val = 0
            for x in dupli:
                val = val + subs[i].text.count(x)
            dis[i][j] = val
            j += 1
            count += 1
        i += 1
    max = np.amax(dis, 1)
    i = 0
    result = []
    while (i < len(subs)):
        result.append(np.where(dis[i] == max[i])[0][0])
        i += 1
    return result





def srtAndSlideTextVector(srtFilename, SlideArray, size):
    subs = pysrt.open(srtFilename, encoding='iso-8859-1')
    i = 0
    dis = np.zeros((len(subs), len(SlideArray)))
    if size == 0:
        tfidfvectoriser = TfidfVectorizer(analyzer='word', stop_words='english')
    else:
        tfidfvectoriser = TfidfVectorizer(analyzer='char', ngram_range=(size, size))
    tfidfvectoriser.fit_transform(pdfArray)
    # TF-IDF of all slide arrays
    slidesVec = []
    for j in range(len(SlideArray) - 1):
        new = []
        new.append(SlideArray[j])
        slidesVec.append(tfidfvectoriser.transform(new).toarray())
        j += 1
    # TF-IDF of all subtitles (based on only pdf as library)
    subsVec = []
    while (i < len(subs)):
        new = []
        new.append(subs[i].text)
        subsVec.append(tfidfvectoriser.transform(new).toarray())
        i += 1
    cx = lambda a, b: np.inner(a, b) / (LA.norm(a) * LA.norm(b))
    i = 0
    final = []
    while (i < len(subsVec)):
        print(i)
        max = 0
        index = 0
        for x in range(len(SlideArray) - 1):
            print(x)
            cosine = cx(subsVec[i], slidesVec[x])
            print(cosine)
            if cosine >= max:
                max = cosine
                index = x
        final.append(index)
        i += 1
    return final


##def srtAndSlidesNeuralCRF(srtArray, slideArray):

def srtAndSlidesSmithWaterman(srtFilename, SlideArray):
    subs = pysrt.open(srtFilename, encoding='iso-8859-1')
    i = 0
    dis = np.zeros((len(subs), len(SlideArray)))
    dis = dis * 1.0
    count = 0

    while (i < len(subs)):
        for j in range(len(SlideArray) - 1):
            dis[i][j] = textdistance.smith_waterman.distance(subs[i].text, SlideArray[j])
            j += 1
            count += 1
        i += 1
    max = np.amax(dis, 1)
    i = 0
    result = []
    while (i < len(subs)):
        result.append(np.where(dis[i] == max[i])[0][0])
        i += 1
    return result


def srtAndCATS(srtFilename, SlideArray, baseDir):
    subs = pysrt.open(srtFilename, encoding='iso-8859-1')
    i = 0
    count = 0

    while (i < len(subs)):
        if not os.path.exists(baseDir + "\\CATS"):
            os.mkdir(baseDir + "\\CATS")
        f = open(baseDir + "\\CATS\\" + str(i) + ".txt", "w")
        for j in range(len(SlideArray) - 1):
            # create file and run jar over it
            sub = re.sub(r'[^a-zA-Z0-9 ]+', '', subs[i].text)
            slide = re.sub(r'[^a-zA-Z0-9 ]+', '', SlideArray[j])
            f.write(sub + '\t' + '\t' + slide + '\n')
            j += 1
            count += 1
        f.close()
        process = subprocess.Popen(["java", "-jar",
                                    "..\\ThesisUpdate-SimpTextAlign\\classes\\artifacts\\simplifiedTextAlignment_jar\\simplifiedTextAlignment.jar",
                                    baseDir + "\\CATS\\" + str(i) + ".txt"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        result = process.communicate()
        i = i + 1
    sleep(10)
    RESULT = []
    for infile in os_sorted(glob.glob(baseDir + "\\CATS\\*.txt_sentence_CWASA")):
        #print(os.stat(infile))
        #print(infile)
        f = open(infile, 'r')
        numbs = []
        while True:
            line = f.readline()
            if not line:
                break
            num = line.split('\t')[-1]
            #print(num)
            numbs.append(float(num.rstrip("\n")))
        f.close()
        #print(numbs)
        RESULT.append(np.argmax(numbs, axis=0))
    #print(RESULT)
    return RESULT


#def srtAndCRF(srtFilename, SlideArray, baseDir):
    #At the moment just use their trained wikipedia and see if it will align
    # Then in another file look at training theirs

def simpleEvaluation(algorithmResult, actualResult):
    i = 0
    total = 0
    correct = 0
    close = 0
    #print(actualResult)
    #print(algorithmResult)
    # close is not correct but within 1 value (+1 or -1)
    while (i < len(algorithmResult) and i < len(actualResult)):
        #print(i)
        if algorithmResult[i] == int(actualResult[i]):
            correct = correct + 1
        if (algorithmResult[i] == int(actualResult[i]) + 1):
            close = close + 1
        if (algorithmResult[i] == int(actualResult[i]) - 1):
            close = close + 1
        total = total + 1
        i = i + 1
    print("Total = " + str(total) + ". Correct = " + str(correct) + ". Close = " + str(close))
    return "Total = " + str(total) + ". Correct = " + str(correct) + ". Close = " + str(close)



if __name__ == "__main__":
    # process = subprocess.Popen(["java", "-jar", "..\\SimpTextAlignCode\\out\\artifacts\\simplifiedTextAlignment_jar\\simplifiedTextAlignment.jar", "Lecture1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    # result = process.communicate()
    # print(result)
    # print("Done")
    #NOT: 17, 20, 21, 22, 23, 24, 25, 47, 75, 77, 91, 92, 97, 104, 105, 106, 107, 108, 109
    outputList = ["Lecture33","Lecture34","Lecture35_c34",
                  "Lecture36_c34","Lecture37","Lecture38_c37","Lecture39",
                  "Lecture40", "Lecture41","Lecture42","Lecture43","Lecture44","Lecture45",
                  "Lecture46","Lecture48","Lecture49","Lecture50",
                  "Lecture51", "Lecture52","Lecture53","Lecture54_c53","Lecture55","Lecture56_c55",
                  "Lecture57", "Lecture58",
                  "Lecture59_c58","Lecture60", "Lecture61", "Lecture62","Lecture63","Lecture64","Lecture65","Lecture66",
                  "Lecture67", "Lecture68","Lecture69","Lecture70",
                  "Lecture71", "Lecture72","Lecture73","Lecture74","Lecture76","Lecture78",
                  "Lecture79","Lecture80","Lecture81","Lecture83","Lecture84","Lecture85"

                  ]
    """ "Lecture95","Lecture96", "Lecture98", "Lecture99",
                  "Lecture100", "Lecture101", "Lecture102", "Lecture103", "Lecture110",
                  "Lecture111", "Lecture112", "Lecture113", "Lecture114", "Lecture115",
                  "Lecture116", "Lecture117", "Lecture118", "Lecture119"
    "Lecture114", "Lecture115",
                  "Lecture116", "Lecture117", "Lecture118", "Lecture119"
    "Lecture90",
                    "Lecture93","Lecture94","Lecture95","Lecture96","Lecture98", "Lecture99",
                  "Lecture100","Lecture101","Lecture102","Lecture103", "Lecture110",
                  "Lecture111", "Lecture112", "Lecture113",
    "Lecture89","Lecture90",
    "Lecture83","Lecture84","Lecture85","Lecture86",
                  "Lecture87", "Lecture88",
                  "Lecture61", "Lecture62","Lecture63","Lecture64","Lecture65","Lecture66",
                  "Lecture67", "Lecture68",
                  "Lecture69","Lecture70",
                  "Lecture71", "Lecture72","Lecture73","Lecture74","Lecture76","Lecture78",
                  "Lecture79","Lecture80",
                  "Lecture81", "Lecture82",
"Lecture1", "Lecture2","Lecture3", "Lecture4",
                  "Lecture5", "Lecture6","Lecture7", "Lecture8","Lecture9","Lecture10"   "Lecture98", "Lecture99",
                  "Lecture100","Lecture101","Lecture102","Lecture103", "Lecture110",
                  "Lecture111", "Lecture112", "Lecture113", "Lecture114", "Lecture115",
                  "Lecture116", "Lecture117", "Lecture118", "Lecture119"
                   "Lecture93","Lecture94","Lecture95","Lecture96",
    "Lecture31","Lecture32_c31","Lecture33","Lecture34","Lecture35_c34",
                  "Lecture36_c34",
                  "Lecture37",
                  "Lecture38_c37","Lecture39",
                  "Lecture40", "Lecture41","Lecture42","Lecture43","Lecture44","Lecture45",
                  "Lecture46",
                  "Lecture48",
                  "Lecture49","Lecture50",
                  "Lecture51", "Lecture52","Lecture53","Lecture54_c53","Lecture55","Lecture56_c55",
                  "Lecture57", "Lecture58",
                  "Lecture59_c58","Lecture60",
                  "Lecture61", "Lecture62","Lecture63","Lecture64","Lecture65","Lecture66",
                  "Lecture67", "Lecture68",
                  "Lecture69","Lecture70",
                  "Lecture71", "Lecture72","Lecture73","Lecture74","Lecture76","Lecture78",
                  "Lecture79","Lecture80",
                  "Lecture81", "Lecture82","Lecture83","Lecture84","Lecture85","Lecture86",
                  "Lecture87", "Lecture88",
                  "Lecture89","Lecture90",
    "Lecture1", "Lecture2","Lecture3", "Lecture4", 
                  "Lecture5", "Lecture6","Lecture7", "Lecture8","Lecture9","Lecture10"
                    "Lecture52","Lecture53","Lecture54_c53","Lecture55","Lecture56_c55",
                  "Lecture57", "Lecture58",
                  "Lecture59_c58","Lecture60",
      "Lecture11",
                  "Lecture12","Lecture13",
                  "Lecture14", "Lecture15","Lecture16","Lecture18","Lecture19",  "Lecture26",
                  "Lecture27",
                  "Lecture28","Lecture29_c28",
                  "Lecture30","Lecture31","Lecture32_c31","Lecture33","Lecture34","Lecture35_c34",
                  "Lecture36_c34",
                  "Lecture37",
                  "Lecture38_c37","Lecture39",
                  "Lecture40", "Lecture41","Lecture42","Lecture43","Lecture44","Lecture45",
                  "Lecture46",
                  "Lecture48",
                  "Lecture49","Lecture50",
                  "Lecture51",            
     "Lecture2","Lecture3",
                  "Lecture4", "Lecture5","Lecture6","Lecture7","Lecture8","Lecture9",
                  "Lecture10", "Lecture11",
                  "Lecture12","Lecture13",
                  "Lecture14", "Lecture15","Lecture16","Lecture18","Lecture19",  "Lecture26",
                  "Lecture27",
                  "Lecture28","Lecture29_c28",
                  "Lecture30",           
                  
    "Lecture29_c28", "Lecture32_c31",
                  "Lecture35_c34", "Lecture36_c34", "Lecture38_c37", "Lecture54_c53",
                  "Lecture56_c55", "Lecture59_c58"]
    """
    outputList1 = ["Lecture1"]
    for x in outputList1:
        outputLocation = "..\\2_pipeline" + "\\" + x
        outputLocation1 = "..\\0_data" + "\\" + x
        pdfArrayFile = open(outputLocation + "\\Results" + "\\slideArray.txt", "r")
        pdfArrayContent = pdfArrayFile.read()
        pdfArray = pdfArrayContent.split("ENDELEMENT")
        pdfArrayFile.close()

        srt = outputLocation + "\\Results" + "\\generatedTranscriptSRT.srt"
        #srt = outputLocation1 + "\\Transcript-srt.txt"

        truth = outputLocation + "\\Results" + "\\fixedalign.txt"
        truthArray = open(truth)
        truthArray = truthArray.read().splitlines()
        #print(truthArray)

        #print("Jaccard")
        #jaccardresult1 = srtAndSlideTextWordJaccard(srt, pdfArray, 1)
        #evj1 = simpleEvaluation(jaccardresult1, truthArray)
        #wordoverlapresult = srtAndSlideTextWordOverlap(srt, pdfArray)
        #evo = simpleEvaluation(wordoverlapresult, truthArray)
        #print("Vector")
        #vector = srtAndSlideTextVector(srt, pdfArray, 0)
        #evv = simpleEvaluation(vector, truthArray)
        #print("Smith Waterman")
        #sw = srtAndSlidesSmithWaterman(srt, pdfArray)
        #evsw = simpleEvaluation(sw, truthArray)
        #print("CATS")
        cats = srtAndCATS(srt, pdfArray, outputLocation)
        evc = simpleEvaluation(cats, truthArray)


        #resulting = []
        #resulting.append(jaccardresult)
        #resulting.append(wordoverlapresult)
        #resulting.append(vector)
        #resulting.append(cats)
        #resulting.append(sw)

"""
        results = open(outputLocation + "\\resultListJacc.txt", "w")
        for text in resulting:
            results.write("ENDELEMENT")
            for x in text:
                results.write(str(x))
                results.write(",")
        results.close()

        ev = []
        #ev.append(evj)
        #ev.append(evo)
        #ev.append(evv)
        #ev.append(evc)
        #ev.append(evsw)

        ev.append(evj1)
        ev.append(evj2)
        ev.append(evj3)
        ev.append(evj4)
        ev.append(evj5)
        ev.append(evj6)
        ev.append(evj7)
        ev.append(evj8)
        ev.append(evj9)

        results = open(outputLocation + "\\resultEvJacc.txt", "w")
        for text in ev:
            results.write("ENDELEMENT")
            for x in text:
                results.write(str(x))
        results.close()
        """