import json
import os

from annotateSlides import convert_pdf2img
from check_images import checkTextPdf, checkTextPdfCrop
from screenshot_videos import get_frames
from createTranscript import splitSubtitles
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
#    for filename in os.listdir(inputFolder):
#        slideText = checkTextPdfCrop(inputFolder + "\\" + filename)
#        list.append(slideText)
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


def createTimeTranscriptPairing(array, transcript, timing):
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
    dataGroup = ["Lecture1"]

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
        fixedArray = fixNumberOrder(array)

        timingDict = createTimeTranscriptPairing(fixedArray, fixedArray, 10)

        dict = splitSubtitles(timingDict, inputLocation + "\\Transcript-srt.txt")
        textfile = open(outputLocation + "\\Results" + "\\FinalAlignment.txt", "w")
        for text in dict:
            json.dump(dict, textfile)
        textfile.close()
        