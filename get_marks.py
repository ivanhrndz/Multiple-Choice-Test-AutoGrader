import numpy as np
from scipy.stats import gaussian_kde



def score():
	answers=[]
	width = 15
	height = 20
	locations =[10]#, 40, 60, 70, 90]
	for location in locations:
		window=np.array([[5,5,5,2,2,3,3,3,3,2,2,2,1,1,1],[5,5,5,2,2,3,3,3,3,2,2,2,1,1,1],[4,4,4,2,2,3,3,3,3,2,2,2,1,1,1]])
		#window = img[location:location+width,location:location+height]
		summed_window = window.sum(axis=0).round()
		hist = np.repeat(np.arange(width), summed_window, axis=0)
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
		return answers
		
def questioncorrect(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8)
	
def grade(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8).mean()
	
def raw(form,key):
	return np.array([form[i] == key[i] for i in range(len(form))],dtype=np.uint8).sum()	