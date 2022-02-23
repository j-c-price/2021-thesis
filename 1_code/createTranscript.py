import pysrt

def splitSubtitles(timeDictionary, filename, index):
    subs = pysrt.open(filename, encoding='iso-8859-15')
    time = 0
    timeSlideSub = {}
    for i in timeDictionary:
        duration = timeDictionary[i]
        print(time)
        part = subs.slice(starts_after={'seconds': time}, ends_before={'seconds': time + duration})
        timeSlideSub[time] = [index, timeDictionary[i], part.text]
        time = time + duration
        index = index + 1
    return timeSlideSub

if __name__ == "__main__":
    splitSubtitles("Transcript-srt.txt", 1)