import glob
import os
import re
import subprocess
from time import sleep

import NeuralCRF
from NeuralCRF import simplification
import numpy as np
import numpy.linalg as LA
import pysrt
import textdistance
from natsort import os_sorted
from sklearn.feature_extraction.text import TfidfVectorizer


# Compare each line of SRT to a whole slide of ppt text
def srtAndSlideTextWordOverlap(srtFilename, SlideArray):
    subs = pysrt.open(srtFilename)
    i = 0
    dis = np.zeros((len(subs), len(SlideArray)))
    dis = dis * 1.0
    count = 0

    # Jaccard Similarity?
    while (i < len(subs)):
        for j in range(len(SlideArray) - 1):
            dis[i][j] = textdistance.jaccard.distance(subs[i].text, SlideArray[j])
            j += 1
            count += 1
        i += 1
    max = np.amax(dis, 1)
    i = 0
    result = []
    while (i < len(subs)):
        result.append(np.where(dis[i] == max[i])[0][0])
        i += 1
    print(result)


def srtAndSlideTextVector(srtFilename, SlideArray, size):
    # train is the pdf slides, test is the srts
    subs = pysrt.open(srtFilename)
    i = 0
    dis = np.zeros((len(subs), len(SlideArray)))
    dis = dis * 1.0
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
        max = 0
        index = 0
        for x in range(len(SlideArray) - 1):
            print("A")
            print(subsVec[i])
            print(slidesVec[x])
            cosine = cx(subsVec[i], slidesVec[x])
            if cosine >= max:
                max = cosine
                index = x
            final.append(index)
        i += 1
    print(final)


##def srtAndSlidesNeuralCRF(srtArray, slideArray):

def srtAndSlidesSmithWaterman(srtFilename, SlideArray):
    subs = pysrt.open(srtFilename)
    i = 0
    dis = np.zeros((len(subs), len(SlideArray)))
    dis = dis * 1.0
    count = 0

    # Jaccard Similarity?
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
    print(result)


def srtAndCATS(srtFilename, SlideArray, baseDir):
    subs = pysrt.open(srtFilename)
    i = 0
    count = 0

    while (i < len(subs)):
        if not os.path.exists(baseDir + "\\CATS"):
            os.mkdir(baseDir + "\\CATS")
        f = open(baseDir + "\\CATS\\" + str(i) + ".txt", "w")
        for j in range(len(SlideArray) - 1):
            # create file and run jar over it
            # JELENAAA HELLO
            sub = re.sub(r'[^a-zA-Z0-9 ]+', '', subs[i].text)
            slide = re.sub(r'[^a-zA-Z0-9 ]+', '', SlideArray[j])
            f.write(sub + '\t' + '\t' + slide + '\n')
            j += 1
            count += 1
        f.close()
        process = subprocess.Popen(["java", "-jar",
                                    "..\\SimpTextAlignCode\\out\\artifacts\\simplifiedTextAlignment_jar\\simplifiedTextAlignment.jar",
                                    "Lecture1" + "\\CATS\\" + str(i) + ".txt"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        result = process.communicate()
        print(result)
        i = i + 1
    sleep(10)
    RESULT = []
    for infile in os_sorted(glob.glob(baseDir + "\\CATS\\*.txt_sentence_C3G")):
        print(os.stat(infile))
        print(infile)
        f = open(infile, 'r')
        numbs = []
        while True:
            line = f.readline()
            if not line:
                break
            num = line.split('\t')[-1]
            print(num)
            numbs.append(float(num.rstrip("\n")))
        f.close()
        print(numbs)
        RESULT.append(np.argmax(numbs, axis=0))
    print(RESULT)


if __name__ == "__main__":
    # process = subprocess.Popen(["java", "-jar", "..\\SimpTextAlignCode\\out\\artifacts\\simplifiedTextAlignment_jar\\simplifiedTextAlignment.jar", "Lecture1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    # result = process.communicate()
    # print(result)
    # print("Done")

    outputLocation = "..\\2_pipeline" + "\\" + "Lecture1"

    pdfArrayFile = open(outputLocation + "\\Results" + "\\slideArray.txt", "r")
    pdfArrayContent = pdfArrayFile.read()
    pdfArray = pdfArrayContent.split("ENDELEMENT")
    pdfArrayFile.close()

    srt = outputLocation + "\\Results" + "\\generatedTranscriptSRT.srt"

    # srtAndSlideTextWordOverlap(srt, pdfArray)

    # srtAndSlideTextVector(srt, pdfArray, 0)

    # srtAndSlidesSmithWaterman(srt, pdfArray)

    srtAndCATS(srt, pdfArray, outputLocation)
