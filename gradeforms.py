import numpy as np
from PIL import ImageOps
from PIL import Image
import random
from scipy.ndimage.morphology import grey_dilation
import string


def score(img):

	img = Image.fromarray(grey_dilation(np.array(img),(3,3)))
	img = ImageOps.invert(img)
	img=np.array(img)
	img[img > 50] = 255
	img[img <= 50] = 0

	
	width = 16
	height = 120
	id_locations = [(301+(i*18),57) for i in range (8)]
	id_number =""
	for x,y in id_locations:
		window=np.array(img)[y:y+height,x:x+width]
		
		summed_window = (window.sum(axis=1)).round()
		areas = np.linspace(0,height,11).astype(int)
		blocks = []
		for i in range(10):
			block = summed_window[areas[i]:areas[i+1]]
			blocks.append(block.sum())

		blocks = np.array(blocks).astype(float)
		if blocks.max() > 2000:
			position = np.argmax(blocks)
			id_number+=str(position)


	locations = zip([34]*25,np.linspace(212,561,25).round().astype(int))
	locations.extend(zip([140]*25,np.linspace(212,561,25).round().astype(int)))
	locations.extend(zip([250]*25,np.linspace(212,561,25).round().astype(int)))
	locations.extend(zip([366]*25,np.linspace(212,561,25).round().astype(int)))
	answers=[]
	width = 85
	height = 9
	p=1
	
	for x,y in locations:
		window=np.array(img)[y:y+height,x:x+width]
		summed_window = (window.sum(axis=0)/100).round()
		
		areas = np.linspace(0,width,6).astype(int)
		blocks = []
		for i in range(5):
			block = summed_window[areas[i]:areas[i+1]]
			blocks.append(block.sum())
		blocks = np.array(blocks)
		if blocks.max() >= 10:
			position = np.argmax(blocks)
			answers.append(string.ascii_uppercase[position])
		else:
			answers.append("")
	
	return (id_number,answers)
		
def questionscorrect(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8)
	
def grade(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8).mean()*100
	
def raw(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8).sum()	
