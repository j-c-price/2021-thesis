import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip


def transcribe_video(finalWavName, inputVideoName, outputTranscriptName):
    audioclip = AudioFileClip(inputVideoName)
    audioclip.write_audiofile(finalWavName)

    with contextlib.closing(wave.open(finalWavName, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()

    for i in range(0, total_duration):
        with sr.AudioFile(finalWavName) as source:
            audio = r.record(source, offset=i*60, duration=60)
            f = open(outputTranscriptName, "a")
            try:
                f.write(r.recognize_google(audio))
            except:
                print("Unknown word")
            f.write(" ")
        f.close()

if __name__ == "__main__":
    name = "transcribed.wav"
    transcribe_video(name,"Video.mp4")

