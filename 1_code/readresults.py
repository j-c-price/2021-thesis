import os
from statistics import median
import pysrt
def timeAway(algorithmResult, actualResult):
    unique_list = []
    for x in actualResult:
        if x.isdigit():
            x = int(x)
            if x not in unique_list:
                unique_list.append(x)

    print(unique_list)
    listAct = []
    listAlg = []
    for x in unique_list:
        try:
            listAct.append(actualResult.index(str(x)))
            listAlg.append(algorithmResult.index(str(x)))
            #print(algorithmResult.index(str(x)))
            #print(actualResult.index(str(x)))
        except:
            listAlg.append(0)
            #print("0")
    i = 0
    tot = []
    wo = []
    while i < len(listAct):
        #print(listAlg[i] - listAct[i])
        tot.append(abs(listAlg[i] - listAct[i])*10)
        wo.append(abs(0 - listAct[i])*10)
        i = i + 1
    print(tot)
    print(wo)
    print((sum(tot)/len(tot))/60)
    print((sum(wo)/len(wo))/60)
    return sum(tot), sum(wo)

def simpleEvaluation(algorithmResult, actualResult, close):
    i = 0
    total = 0
    correct = 0
    while (i < len(algorithmResult) and i < len(actualResult)):
        if abs(int(algorithmResult[i]) - int(actualResult[i])) <= close:
            correct = correct + 1
        total = total + 1
        i = i + 1
    return total, correct


def simpleEvaluationPerfect(algorithmResult, subs, actualResult, close):
    i = 0
    total = 0
    correct = 0
    # close is not correct but within 1 value (+1 or -1)
    while (i < len(algorithmResult) and i < len(actualResult)):
        index = round((subs[i].start.minutes * 60 + subs[i].start.seconds) / 10)
        if abs(int(algorithmResult[i]) - int(actualResult[index])) <= close:
            correct = correct + 1
        total = total + 1
        i = i + 1
    print("Total = " + str(total) + ". Correct = " + str(correct))
    return total, correct

if __name__ == "__main__":

    outputListLec = ["Lecture1", "Lecture2","Lecture3", "Lecture4",
                  "Lecture5", "Lecture6","Lecture7", "Lecture8","Lecture9","Lecture10", "Lecture11",
                  "Lecture12","Lecture13", "Lecture14", "Lecture15","Lecture16","Lecture18","Lecture19",  "Lecture26",
                  "Lecture27","Lecture28","Lecture29_c28",
                  "Lecture30","Lecture31","Lecture32_c31","Lecture33","Lecture34","Lecture35_c34",
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
    outputListLec1 = ["Lecture1", "Lecture2","Lecture3", "Lecture4",
                  "Lecture5", "Lecture6","Lecture7", "Lecture8","Lecture9","Lecture10", "Lecture11",
                  "Lecture12","Lecture13", "Lecture14", "Lecture15","Lecture16","Lecture18","Lecture19",  "Lecture26",
                  "Lecture27","Lecture28","Lecture29_c28"]
    #removed Lecture82 for Perfect
    outputListConf =["Lecture86", "Lecture87", "Lecture88","Lecture89","Lecture90", "Lecture93","Lecture94",
                  "Lecture95","Lecture96", "Lecture98", "Lecture99",
                  "Lecture100", "Lecture101", "Lecture102", "Lecture103", "Lecture110",
                  "Lecture111", "Lecture112", "Lecture113", "Lecture114", "Lecture115",
                  "Lecture116", "Lecture117", "Lecture118", "Lecture119"
                  ]
    total = 0
    perfect = 0
    close = 0
    numSS = []
    for x in outputListLec:
        """
        print("A")
        #try:
        outputLocation = "..\\2_pipeline" + "\\" + x + "\\SlideScreenshots"
        onlyfiles = next(os.walk(outputLocation))[2]  # dir is your directory path as string
        print(len(onlyfiles))
        numSS.append(len(onlyfiles))

    print(sum(numSS)/len(numSS))
    print(sum(numSS))
    print(median(numSS))
    print(min(numSS))
    print(max(numSS))
"""
        outputLocation = "..\\2_pipeline" + "\\" + x
        videoArrayFile = open(outputLocation + "\\resultList.txt", "r")
        videoArrayContent = videoArrayFile.read()
        videoArray = videoArrayContent.split("ENDELEMENT")
        videoArrayFile.close()
        outputLocation1 = "..\\0_data" + "\\" + x
        srt = outputLocation1 + "\\Transcript-srt.txt"
        subs = pysrt.open(srt, encoding='iso-8859-1')

        try:
            sent = videoArray[3].split(',')[:-1]
        except:
            #print("Failed")
            pass
        truth = outputLocation + "\\Results" + "\\fixedalign.txt"
        truthArray = open(truth)
        truthArray = truthArray.read().splitlines()
        #print(timeAway(sent, truthArray))
        ev_total, ev_correct = simpleEvaluation(sent, truthArray, 0)
        #ev_total, ev_correct = simpleEvaluationPerfect(sent,subs, truthArray, 10)


        total = total + ev_total
        perfect = perfect + ev_correct
        pc = (ev_correct/ev_total)*100
        print(str(x) + "Total:" + str(ev_total) + "  " + str(ev_correct) + "  " + str(pc))
        #except:
            #print("no")
            #pass
    print(total)
    print(close + perfect)
    print(((close + perfect)/total)*100)