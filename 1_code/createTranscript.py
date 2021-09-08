import pysrt

def splitSubtitles(timeDictionary, filename):
    subs = pysrt.open(filename)
    time = 0
    timeSlideSub = {}
    for i in timeDictionary:
        duration = timeDictionary[i]
        print(time)
        part = subs.slice(starts_after={'seconds': time}, ends_before={'seconds': time + duration})
        timeSlideSub[time] = [timeDictionary[i], part.text]
        time = time + duration
    return timeSlideSub

if __name__ == "__main__":
    splitSubtitles("Transcript-srt.txt", 1)