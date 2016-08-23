from PIL import Image
import numpy as np
from skimage.feature import match_template

def identify(fname):
	img = Image.open('fname').convert("L")
	
	#load QR code
	QR = Image.open("QR.png").convert("L")
	
	#match the QR code
	result = match_template(np.array(img), np.array(QR))
	
	ij = np.unravel_index(np.argmax(result), result.shape)
	x, y = ij[::-1]