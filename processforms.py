import  glob
from PIL import Image
import numpy as np
from pyirt._pyirt import irt
from alignforms import process_image
from get_marks import score,questionscorrect,grade,raw



aligned_forms=[]
from collections import defaultdict
grades = defaultdict(dict)
import matplotlib.pyplot as plt
def process_forms():
	forms = glob.glob("formstograde\\*.png")
	key = glob.glob("key\\*.png")[0]
	key_scored = score(Image.open(key).convert("L"))[1]
	for fname in forms:
		form = Image.open(fname).convert("L").rotate(15,expand=True)
		#reference_template = Image.open("templates\\template.png").convert("L")
		aligned = process_image(form)
		plt.imshow(aligned)
		plt.show()
		id,scored = score(aligned)
		grades[id]['grade'] = grade(scored,key_scored)
		grades[id]['raw'] = raw(scored,key_scored)
		grades[id]['questionscorrect'] =  questionscorrect(scored,key_scored)
	return grades
	
def make_summary_report(grades,fname="graded_summary.csv"):
	with open(fname,"ab") as g:
		g.write("id,score\r\n")
	for id in grades.iterkeys():
		responses = form['responses']
		raw = np.sum(responses)
		percentage = np.mean(responses)
		with open(fname,"ab") as g:
			g.write("%s,%s,%s\r\n") % (id,grades[id]['raw'],grades[id]['grade'])
	
def make_detailed_report(grades,fname="graded_detailed.csv"):
	with open(fname,"ab") as g:
		number_questions = len(grades[0])
		header = ["Q%s" % i for i in range(1,len(grades[0]))+1]
		g.write("id,"+",".join(header)+"\r\n")
	for id in grades.iterkeys():
		responses = ",".join([str(x) for x in grades[id]['questionscorrect']])
		with open(fname,"ab") as g:
			g.write("%s,%s\r\n" % (id,responses))


def make_item_report(grades,fname="graded_item.csv"):
	with open(fname,"ab") as g:
		number_questions = len(grades[0])
		g.write("item,difficulty,discrimination,guessability\r\n")
	response_list=[]
	for id in grades.iterkeys():
		for item in range(len(grades[id]['questionscorrect'])):
			response_list.append((id,item,grades[id]['questionscorrect'][item]))
		item_param,user_param = irt(response_list)
	i=1
	for item in item_param:
		with open(fname,"ab") as g:
			g.write("Q%s,%s,%s,%s\r\n" % (i,item['difficulty'],item['discrimination'],item['guessability']))
		i+=1

