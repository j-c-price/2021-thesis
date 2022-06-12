import json
import os

from annotateSlides import convert_pdf2img
from check_images import checkTextPdf, checkTextPdfCrop
from screenshot_videos import get_frames
from createTranscript import splitSubtitles
from transcribeAVideo import transcribe_video
import Levenshtein
#What needs to get done?
#First, we should manage splitting the slide pdfs
#Then we should annotate all the slides
#We should take screenshots of the videos
#We should then annotate all the video screenshots

#We then need to work out what the start and end time of the pdf slide is according to the video

#We then need to parse in the transcript text with the time
#We need to find which sentence belongs within the slide frames
#And align each sentence of transcript to slide 0 - x (the slides)


def splitSlides(input, output):
    output = output + "\\SlideScreenshots"
    input = input + "\\Slides.pdf"
    try:
        # creating a folder named data
        if not os.path.exists(output):
            os.makedirs(output)

            # if not created then raise error
    except OSError:
        print('Error! Could not create a directory')

    convert_pdf2img(input, output)

def textOnSlide(inputFolder):
    list = []
#   for filename in os.listdir(inputFolder):
#       slideText = checkTextPdf(inputFolder + "\\" + filename)
#       list.append(slideText)
    i = 0
    while (os.path.exists(inputFolder + "\\page" + str(i) + ".jpg")):
        slideText = checkTextPdf(inputFolder + "\\page" + str(i) + ".jpg")
        list.append(slideText)
        i = i+1
    return list

def textOnSlideCrop(inputFolder):
    list = []
    i = 0
    while (os.path.exists(inputFolder + "\\" + str(i) + ".jpg")):
        slideText = checkTextPdfCrop(inputFolder + "\\" + str(i) + ".jpg")
        list.append(slideText)
        i = i+1
    return list

def matchSlideToVideo(slideArray, VideoArray):
    SlideMatch = []
    videoIndex = 0
    for i in VideoArray:
        distanceList = []
        slideIndex = 0
        for j in slideArray:
            ## Similarity Measure:
            i_tokens = set(i.lower().split())
            j_tokens = set(j.lower().split())
            if len(i_tokens.union(j_tokens)) != 0:
                distance = len(i_tokens.intersection(j_tokens))/len(i_tokens.union(j_tokens))
            else:
                distance = 10000
            distanceList.append(distance)
            slideIndex = slideIndex+1
        SlideWithShortestDistance = distanceList.index(max(distanceList))
        SlideMatch.append(SlideWithShortestDistance)
        videoIndex = slideIndex+1
    print(SlideMatch)
    return SlideMatch

def fixNumberOrder(array):
    newArray = []
    currentSlide = 0
    for i in array:
        if abs(currentSlide - i) > 2:
            newArray.append(currentSlide)
        else:
            currentSlide = i
            newArray.append(i)
    return newArray


def createTimeTranscriptPairing(array, timing):
    arrayTime = {}
    current_i = 0
    count = 1
    total = 0
    for i in array:
        if current_i == i:
            count = count + 1
        else:
            arrayTime[current_i] = count * timing
            total = total + count * timing
            count = 1
            current_i = i
        if array[-1] == current_i:
            arrayTime[current_i] = count * timing
    return arrayTime


if __name__ == "__main__":
    #Work with 10
    #dataGroupDone = ["Lecture1", "Lecture2",
    #             "Lecture3", "Lecture4","Lecture5",
    #             "Lecture6","Lecture7","Lecture8",
    #             "Lecture9","Lecture10","Lecture11","Lecture12",
    #             "Lecture13","Lecture14","Lecture15","Lecture16",
    #             "Lecture17","Lecture18","Lecture19","Lecture20","Lecture21",
    #             "Lecture22","Lecture23","Lecture24","Lecture25","Lecture26",
     #            "Lecture27","Lecture28","Lecture29_c28","Lecture30","Lecture31",
     #            "Lecture32_c31", "Lecture33", "Lecture34", "Lecture35_c34",
     #            "Lecture36_c34", "Lecture37","Lecture38_c37", "Lecture39",
    #             "Lecture40", "Lecture41", "Lecture42", "Lecture43", "Lecture44",
    #             "Lecture45", "Lecture46", "Lecture47", "Lecture48", "Lecture49",
    #             "Lecture50", "Lecture51", "Lecture52", "Lecture53", "Lecture54_c53",
    #             "Lecture55", "Lecture56_c55", "Lecture57", "Lecture58", "Lecture59_c58",
    #             "Lecture60", "Lecture61", "Lecture62", "Lecture63", "Lecture64",
    #             "Lecture65", "Lecture66", "Lecture67", "Lecture68", "Lecture69",
    #             "Lecture70", "Lecture71", "Lecture72", "Lecture73", "Lecture74",
    #             "Lecture75", "Lecture76", "Lecture77", "Lecture78", "Lecture79",
    #             "Lecture80", "Lecture81", "Lecture82", "Lecture83", "Lecture84"]
    dataGroup = ["Lecture86", "Lecture87", "Lecture88", "Lecture89", "Lecture90", "Lecture91",
                 "Lecture92", "Lecture93", "Lecture94", "Lecture95", "Lecture96", "Lecture97",
                 "Lecture98", "Lecture99", "Lecture100", "Lecture101", "Lecture102", "Lecture103",
                 "Lecture104", "Lecture105", "Lecture106", "Lecture107", "Lecture108", "Lecture109",
                 "Lecture110", "Lecture111", "Lecture112", "Lecture113", "Lecture114", "Lecture115",
                 "Lecture116", "Lecture117", "Lecture118", "Lecture119"]

    dataGroup2 = ["Lecture1", "Lecture2",
                 "Lecture3", "Lecture4","Lecture5",
                 "Lecture6","Lecture7","Lecture8",
                 "Lecture9","Lecture10","Lecture11","Lecture12",
                 "Lecture13","Lecture14", "Lecture26",
                 "Lecture27","Lecture28","Lecture29_c28","Lecture30","Lecture31",
                 "Lecture32_c31", "Lecture33", "Lecture34", "Lecture35_c34",
                 "Lecture36_c34", "Lecture37","Lecture38_c37", "Lecture39",
                 "Lecture40", "Lecture41", "Lecture42", "Lecture43", "Lecture44",
                 "Lecture45", "Lecture46", "Lecture47", "Lecture48", "Lecture49",
                 "Lecture50", "Lecture51", "Lecture52", "Lecture53", "Lecture54_c53",
                 "Lecture55", "Lecture56_c55", "Lecture57", "Lecture58", "Lecture59_c58",
                 "Lecture60", "Lecture61", "Lecture62", "Lecture63", "Lecture64",
                 "Lecture65", "Lecture66", "Lecture67", "Lecture68", "Lecture69",
                 "Lecture70", "Lecture71", "Lecture72", "Lecture73", "Lecture74",
                 "Lecture76", "Lecture78", "Lecture79",
                 "Lecture80", "Lecture81", "Lecture82", "Lecture83"]
    dataGroup1 = ["Lecture1", "Lecture2",
                 "Lecture3", "Lecture4","Lecture5",
                 "Lecture6","Lecture7","Lecture8",
                 "Lecture9","Lecture10","Lecture11","Lecture12",
                 "Lecture13","Lecture14","Lecture15","Lecture16",
                 "Lecture17","Lecture18","Lecture19","Lecture20","Lecture21",
                 "Lecture22","Lecture23","Lecture24","Lecture25","Lecture26",
                 "Lecture27","Lecture28","Lecture29_c28","Lecture30","Lecture31",
                 "Lecture32_c31", "Lecture33", "Lecture34", "Lecture35_c34",
                 "Lecture36_c34", "Lecture37","Lecture38_c37", "Lecture39",
                 "Lecture40", "Lecture41", "Lecture42", "Lecture43", "Lecture44",
                 "Lecture45", "Lecture46", "Lecture47", "Lecture48", "Lecture49",
                 "Lecture50", "Lecture51", "Lecture52", "Lecture53", "Lecture54_c53",
                 "Lecture55", "Lecture56_c55", "Lecture57", "Lecture58", "Lecture59_c58",
                 "Lecture60", "Lecture61", "Lecture62", "Lecture63", "Lecture64",
                 "Lecture65", "Lecture66", "Lecture67", "Lecture68", "Lecture69",
                 "Lecture70", "Lecture71", "Lecture72", "Lecture73", "Lecture74",
                 "Lecture75", "Lecture76", "Lecture77", "Lecture78", "Lecture79",
                 "Lecture80", "Lecture81", "Lecture82", "Lecture83", "Lecture84", "Lecture85"]

    for i in dataGroup:
        inputLocation = "..\\0_data" + "\\" + i
        outputLocation = "..\\2_pipeline" + "\\" + i
        print(inputLocation)

        if not os.path.exists(outputLocation + "\\Results"):
            os.makedirs(outputLocation + "\\Results")

            #split Slides
            splitSlides(inputLocation, outputLocation)

            #text on each slide
            SlideText = textOnSlide(outputLocation + "\\SlideScreenshots")
            textfile = open(outputLocation + "\\Results" + "\\slideArray.txt", "w")
            for text in SlideText:
                textfile.write(text + "ENDELEMENT")
            textfile.close()

            #screenshots of videos
            get_frames(inputLocation + "\\Video.mp4", outputLocation + "\\VideoScreenshots", 10)

            #Create a transcription - do this later
            #transcribe_video(outputLocation + "\\Video.wav",
            #                 inputLocation + "\\Video.mp4",
            #                 outputLocation + "\\Results" + "\\generatedTranscript.txt",
            #                 outputLocation + "\\Results" + "\\genSRT.srt")

            #text on each screenshot
            SlideText = textOnSlideCrop(outputLocation + "\\VideoScreenshots")
            textfile = open(outputLocation + "\\Results" + "\\videoArray.txt", "w")
            for text in SlideText:
                textfile.write(text + "ENDELEMENT")
            textfile.close()

        pdfArrayFile = open(outputLocation + "\\Results" + "\\slideArray.txt", "r")
        pdfArrayContent = pdfArrayFile.read()
        pdfArray = pdfArrayContent.split("ENDELEMENT")
        pdfArrayFile.close()

        videoArrayFile = open(outputLocation + "\\Results" + "\\videoArray.txt", "r")
        videoArrayContent = videoArrayFile.read()
        videoArray = videoArrayContent.split("ENDELEMENT")
        videoArrayFile.close()

        array = matchSlideToVideo(pdfArray, videoArray)
        #fixedArray = fixNumberOrder(array)
        textfile = open(outputLocation + "\\Results" + "\\alignmentUnfixedArray.txt", "w")
        for text in array:
            textfile.write(str(text) + "\n")
        textfile.close()

        # #Read in fixed align
        textfile = open(outputLocation + "\\Results" + "\\fixedalign.txt", "r")
        fixedalignarray = []
        for text in textfile:
             fixedalignarray.append(int(text.rstrip("\n")))
        textfile.close()
        # print(fixedalignarray)
        #
        timingDict = createTimeTranscriptPairing(fixedalignarray, 10)
        #
        dict = splitSubtitles(timingDict, inputLocation + "\\Transcript-srt.txt", fixedalignarray[0])
        textfile = open(outputLocation + "\\Results" + "\\FinalAlignmentBestSRT.txt", "w")
        dict2 = splitSubtitles(timingDict, outputLocation + "\\Results" + "\\generatedTranscriptSRT.srt", fixedalignarray[0])
        #
        json.dump(dict, textfile)
        textfile.close()
        #
        textfile = open(outputLocation + "\\Results" + "\\FinalAlignmentPoorSRT.txt", "w")
        #
        json.dump(dict2,textfile)
        textfile.close()
