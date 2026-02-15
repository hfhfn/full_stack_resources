#coding:utf-8
from PIL import Image
import pytesseract


# im = Image.open('test.jpg')
im = Image.open('getimage.jpg')

result = pytesseract.image_to_string(im)
print(result)