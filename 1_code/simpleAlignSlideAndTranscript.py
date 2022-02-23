import string
import pysrt

from punctuator import Punctuator

#What do we need to do
# read in the slides and the transcripts
# Work out which slides belong to which chunk of the transcript


# Very simple - i.e. don't care about fix - just check the close ness of a sentence to a slide
def compare_distance(arraySentences, arraySummaryTexts):
        SlideMatch = []
        for i in arraySentences:
                #print("A\n")
                distanceList = []
                slideIndex = 0
                for j in arraySummaryTexts:
                        ## Similarity Measure:
                        i_tokens = set(i.lower().split())
                        j_tokens = set(j.lower().split())
                        if len(i_tokens.union(j_tokens)) != 0:
                                distance = len(i_tokens.intersection(j_tokens)) / len(i_tokens.union(j_tokens))
                        else:
                                distance = 10000
                        distanceList.append(distance)
                        slideIndex = slideIndex + 1
                SlideWithShortestDistance = distanceList.index(max(distanceList))
                SlideMatch.append(SlideWithShortestDistance)
        print(SlideMatch)
        return SlideMatch


if __name__ == "__main__":

        SlideLocation = "..\\2_pipeline\\Lecture1\\Results\\SlideArray.txt"

        pdfArrayFile = open(SlideLocation)
        pdfArrayContent = pdfArrayFile.read()
        pdfArray = pdfArrayContent.split("ENDELEMENT")
        pdfArrayFile.close()


        TranscriptLocation = "..\\2_pipeline\\Lecture1\\Results\\generatedTranscriptSRT.srt"
        transcriptFile = open(TranscriptLocation)
        transcriptContent = transcriptFile.read()
        transcriptFile.close()

        subs = pysrt.open(TranscriptLocation)
        subArray = []
        i = 0
        for a in subs:
                i = i+1
                print(a.text)
                subArray.append(a.text)
        print(i)
        match = compare_distance(subArray, pdfArray)
        print(len(match))

