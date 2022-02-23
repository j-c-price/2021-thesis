import datetime
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import srt


def transcribe_video(finalWavName, inputVideoName, outputTranscriptName, outputSRTName):
    audioclip = AudioFileClip(inputVideoName)
    audioclip.write_audiofile(finalWavName)

    with contextlib.closing(wave.open(finalWavName, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()

    transcriptions = []
    index = 0

    for i in range(0, total_duration*6):
        with sr.AudioFile(finalWavName) as source:
            audio = r.record(source, offset=i*10, duration=10)
            f = open(outputTranscriptName, "a")
            try:
                k = r.recognize_google(audio)
                f.write(k)
                transcriptions.append(srt.Subtitle(index, datetime.timedelta(0, i*10,0), datetime.timedelta(0, (i+1)*10, 0), k))
                index += 1
            except:
                print("Unknown word")
            f.write(" ")
        f.close()
    end_srt = srt.compose(transcriptions)
    f1 = open(outputSRTName, "a")
    f1.write(end_srt)


if __name__ == "__main__":
    name = "transcribed.wav"
    fin = "..\\2_pipeline\\Lecture1\\Results\\generatedTranscriptSRT.srt"

   # ["Lecture1", "Lecture2",
    # "Lecture3", "Lecture4", "Lecture5",
    # "Lecture6", "Lecture7", "Lecture8",
    # "Lecture9", "Lecture10", "Lecture11", "Lecture12",
    ## "Lecture13", "Lecture14", "Lecture15", "Lecture16",
    ## "Lecture17", "Lecture18", "Lecture19", "Lecture20", "Lecture21",
    ## "Lecture22", "Lecture23", "Lecture24", "Lecture25"
    ##"Lecture26",
    ##"Lecture27", "Lecture28", "Lecture29_c28", "Lecture30", "Lecture31",
    ##"Lecture32_c31", "Lecture33", "Lecture34", "Lecture35_c34",
    ##"Lecture36_c34", "Lecture37", "Lecture38_c37", "Lecture39",
   ## "Lecture40", "Lecture41", "Lecture42", "Lecture43", "Lecture44",
   ## "Lecture45", "Lecture46", "Lecture47", "Lecture48", "Lecture49",
  ##  "Lecture50", "Lecture51", "Lecture52", "Lecture53", "Lecture54_c53",
  ##  "Lecture55", "Lecture56_c55", "Lecture57", "Lecture58", "Lecture59_c58",
  ##  "Lecture60", "Lecture61", "Lecture62", "Lecture63", "Lecture64",
  ##  "Lecture65", "Lecture66", "Lecture67", "Lecture68", "Lecture69",
  ##  "Lecture70", "Lecture71", "Lecture72", "Lecture73", "Lecture74",
  ##  "Lecture75",

    dataGroup1 = [ "Lecture76", "Lecture78", "Lecture79",
                 "Lecture80", "Lecture81", "Lecture82", "Lecture83", "Lecture84"]

    for i in dataGroup:
        inputLocation = "..\\0_data" + "\\" + i
        outputLocation = "..\\2_pipeline" + "\\" + i
        transcribe_video(outputLocation + "\\wav1.wav", inputLocation + "\\Video.mp4",
                          outputLocation + "\\Results\\" + "generatedTranscript.txt",
                         outputLocation + "\\Results\\" + "generatedTranscriptSRT.srt")
