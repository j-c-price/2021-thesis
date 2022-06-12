import sys
sys.path.append("..\\massalign\\massalign")
from core import *

if __name__ == "__main__":
    #Get files to align:
    file1 = str(sys.argv[1])
    file2 = str(sys.argv[2])
    print(file1)
    print(file2)

    #Train model over them:
    model = TFIDFModel([file1, file2], "..//massalign//sample_data//stop_words.txt")

    #Get paragraph aligner:
    paragraph_aligner = VicinityDrivenParagraphAligner(similarity_model=model, acceptable_similarity=0.3)

    #Get MASSA aligner:
    m = MASSAligner()

    #Get paragraphs from the document:
    p1s = m.getParagraphsFromDocument(file1)
    p2s = m.getParagraphsFromDocument(file2)

    #Align paragraphs:
    alignments, aligned_paragraphs = m.getParagraphAlignments(p1s, p2s, paragraph_aligner)

    #Display paragraph alignments:
    m.visualizeParagraphAlignments(p1s, p2s, alignments)
    m.visualizeListOfParagraphAlignments([p1s, p1s], [p2s, p2s], [alignments, alignments])