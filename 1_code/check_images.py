try:
    from PIL import Image
except ImportError:
    import image
import pytesseract


# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
# # Simple image to string
# print(pytesseract.image_to_string(Image.open('..\\2_pipeline\\VidScreenshots\\0.jpg')))
#
# # List of available languages
# print(pytesseract.get_languages(config=''))
#
# # In order to bypass the image conversions of pytesseract, just use relative or absolute image path
# # NOTE: In this case you should provide tesseract supported images or tesseract will return error
# print(pytesseract.image_to_string('test.png'))
#
# # Batch processing with a single file containing the list of multiple image file paths
# print(pytesseract.image_to_string('images.txt'))
#
# # Timeout/terminate the tesseract job after a period of time
# try:
#     print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
#     print(pytesseract.image_to_string('test.jpg', timeout=0.5)) # Timeout after half a second
# except RuntimeError as timeout_error:
#     # Tesseract processing is terminated
#     pass
#
# # Get bounding box estimates
# print(pytesseract.image_to_boxes(Image.open('test.png')))
#
# # Get verbose data including boxes, confidences, line and page numbers
# print(pytesseract.image_to_data(Image.open('test.png')))
#
# # Get information about orientation and script detection
# print(pytesseract.image_to_osd(Image.open('test.png')))
#
# # Get a searchable PDF
# pdf = pytesseract.image_to_pdf_or_hocr('test.png', extension='pdf')
# with open('test.pdf', 'w+b') as f:
#     f.write(pdf) # pdf type is bytes by default
#
# # Get HOCR output
# hocr = pytesseract.image_to_pdf_or_hocr('test.png', extension='hocr')
#
# # Get ALTO XML output
# xml = pytesseract.image_to_alto_xml('test.png')
def checkTextPdf(inputFile):
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    im = Image.open(inputFile)
    text = pytesseract.image_to_string(im)
   # if len(text) == 0:
   #     text = "NOTHING SEEN"
    return text

def checkTextPdfCrop(inputFile):
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    im = Image.open(inputFile)
    im1 = im.crop((20, 10, 500, 300))
    im1.save(inputFile)
    text = pytesseract.image_to_string(im1)
    #if len(text) == 0:
    #    text = "NOTHING SEEN"
    return text

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
    # Simple image to string

    image = '..\\2_pipeline\\VidScreenshots\\0.jpg'
    im = Image.open(image)

    im1 = im.crop((20, 10, 450, 300))
    im1.save('..\\2_pipeline\\VidScreenshots\\0_cropped.jpg')
    im1.show()
    text = pytesseract.image_to_string(im1)
    print(text[0:100])
    image = 'Slides_page1.png'
    im = Image.open(image)
    text = pytesseract.image_to_string(im)
    print(text[0:100])