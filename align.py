from PIL import Image
import numpy as np
from skimage.feature import match_template

def align(fname):
	img = Image.open('fname').convert("L")
	
	#identify form