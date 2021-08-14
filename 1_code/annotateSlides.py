import fitz
import sys
from typing import Tuple
import os
try:
    from PIL import Image
except ImportError:
    import image
import pytesseract

def convert_pdf2img(input_file: str, output_folder: str):
    """Converts pdf to image and generates a file by page"""
    # Open the document
    pdfIn = fitz.open(input_file)
    output_files = []
    try:
        # creating a folder named data
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

            # if not created then raise error
    except OSError:
        print('Error! Could not create a directory')

    # Iterate throughout the pages
    for pg in range(pdfIn.pageCount):
        # Select a page
        page = pdfIn[pg]
        rotate = int(0)
        # PDF Page is converted into a whole picture 1056*816 and then for each picture a screenshot is taken.
        # zoom = 1.33333333 -----> Image size = 1056*816
        # zoom = 2 ---> 2 * Default Resolution (text is clear, image text is hard to read)    = filesize small / Image size = 1584*1224
        # zoom = 4 ---> 4 * Default Resolution (text is clear, image text is barely readable) = filesize large
        # zoom = 8 ---> 8 * Default Resolution (text is clear, image text is readable) = filesize large
        zoom_x = 2
        zoom_y = 2
        # The zoom factor is equal to 2 in order to make text clear
        # Pre-rotate is to rotate if needed.
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        output_file = output_folder + '\\' "page" + str(pg) + '.jpg'
        pix.writePNG(output_file)
        output_files.append(output_file)
    pdfIn.close()
    return output_files
if __name__ == "__main__":
    convert_pdf2img("..\\0_data\\Lecture1\\Slides.pdf", "..\\2_pipeline\\PdfScreenshots")
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    # Simple image to string
