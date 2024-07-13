import cv2
import numpy as np
import pytesseract
from PIL import Image

def get_string(img_path):
    
    result = pytesseract.image_to_string(Image.open(img_path))
    print('result: ',result)


get_string('index.jpeg')
print ("------ Done -------")