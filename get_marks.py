import numpy as np
from scipy.stats import gaussian_kde
from PIL import ImageOps
from PIL import Image
import random

def score(img):
	img = ImageOps.invert(img)


	
	width = 16
	height = 120
	id_locations = [(301+(i*18),57) for i in range (8)]
	id_number =""
	for x,y in id_locations:
		window=np.array(img)[y:y+height,x:x+width]

		summed_window = (window.sum(axis=1)/100).round()
		hist = np.repeat(np.arange(height), summed_window, axis=0)
		#hist = random.sample(hist, 1000)
		density = gaussian_kde(hist)
		max_area = hist[np.argmax(density.evaluate(hist))]
		if max_area >= ((height*0)/ 11.0) and max_area <= ((height*1)/ 11.0):
			id_number+="0"
		elif max_area >= ((height*1)/ 11.0) and max_area <= ((height*2)/ 11.0):
			id_number+="1"
		elif max_area >= ((height*2)/ 11.0) and max_area <= ((height*3)/ 11.0):
			id_number+="2"
		elif id_number >= ((height*3)/ 11.0) and max_area <= ((height*4)/ 11.0):
			id_number+="3"
		elif max_area >= ((height*4)/ 11.0) and max_area <= ((height*5)/ 11.0):
			id_number+="4"
		elif max_area >= ((height*5)/ 11.0) and max_area <= ((height*6)/ 11.0):
			id_number+="5"
		elif max_area >= ((height*6)/ 11.0) and max_area <= ((height*7)/ 11.0):
			id_number+="6"
		elif max_area >= ((height*7)/ 11.0) and max_area <= ((height*8)/ 11.0):
			id_number+="7"
		elif max_area >= ((height*8)/ 11.0) and max_area <= ((height*9)/ 11.0):
			id_number+="8"
		else: 
			id_number+="9"
	print id_number
	locations = zip([34]*25,np.linspace(212,561,25).round())
	locations.extend(zip([140]*25,np.linspace(212,561,25).round()))
	locations.extend(zip([250]*25,np.linspace(212,561,25).round()))
	locations.extend(zip([366]*25,np.linspace(212,561,25).round()))
	answers=[]
	width = 85
	height = 9
	p=1
	for x,y in locations:
		window=np.array(img)[y:y+height,x:x+width]
		#window = img[location:location+width,location:location+height]
		summed_window = (window.sum(axis=0)/100).round()
		hist = np.repeat(np.arange(width), summed_window, axis=0)
		#hist = random.sample(hist, 1000)
		density = gaussian_kde(hist)
		max_area = hist[np.argmax(density.evaluate(hist))]

		if max_area >= ((width*0)/ 5.0) and max_area <= ((width*1)/ 5.0):
			answers.append("A")
		elif max_area >= ((width*1)/ 5.0) and max_area <= ((width*2)/ 5.0):
			answers.append("B")
		elif max_area >= ((width*2)/ 5.0) and max_area <= ((width*3)/ 5.0):
			answers.append("C")
		elif max_area >= ((width*3)/ 5.0) and max_area <= ((width*4)/ 5.0):
			answers.append("D")
		else: 
			answers.append("E")
	
	return (id_number,answers)
		
def questionscorrect(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8)
	
def grade(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8).mean()*100
	
def raw(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8).sum()	
