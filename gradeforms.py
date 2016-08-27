import  glob
from PIL import Image
import numpy as np
from pyirt._pyirt import irt
from get_marks import score,questionscorrect,grade,raw
from alignforms import align_image


aligned_forms=[]
from collections import defaultdict


def process_forms():
	forms = glob.glob("formstograde\\*.png")
	key = glob.glob("key\\*.png")[0]
	key_scored = score(align_image(Image.open(key).convert("L")))[1]
	n_forms=0.0
	responses = defaultdict(dict)
	for fname in forms:
		
		aligned = align_image(Image.open(fname).convert("L"))
		id,scored = score(aligned)
		responses[id] = scored
		n_forms+=1

	transposed = zip(*responses.values())

	for i in range(1,len(transposed)):
		n_blanks = transposed[-i].count("")
		if (n_blanks  / n_forms) < .95:
			break

	#reduced_responses = zip(*zip(*transposed[:-(i)]))
	reduced_responses = zip(*transposed[:-i+1])
	responses = dict(zip(responses.keys(),reduced_responses))
	
	grades=defaultdict(dict)
	for id,response in responses.iteritems():
		grades[id]['responses']=response
		grades[id]['grade'] = grade(response,key_scored)
		grades[id]['raw'] = raw(response,key_scored)
		grades[id]['questionscorrect'] =  questionscorrect(response,key_scored)
	return grades
	
def make_summary_report(grades,fname="graded_summary.csv"):
	with open(fname,"wb") as g:
		g.write("id,raw,score\r\n")
		for id in grades.iterkeys():
			g.write("%s,%s,%s\r\n" % (id,grades[id]['raw'],grades[id]['grade']))
	
def make_detailed_report(grades,fname="graded_detailed.csv"):
	with open(fname,"wb") as g:
		number_questions = len(grades.values()[0]['responses'])
		header = ["Q%s" % i for i in range(1,number_questions+1)]
		g.write("id,"+",".join(header)+"\r\n")
		for id in grades.iterkeys():
			responses = ",".join([str(x) for x in grades[id]['questionscorrect']])
			g.write("%s,%s\r\n" % (id,responses))


def make_item_report(grades,fname="graded_item.csv"):
	with open(fname,"wb") as g:
		number_questions = len(grades.values()[0]['responses'])
		g.write("item,difficulty,discrimination\r\n")
		response_list=[]
		for id in grades.iterkeys():
			for item in range(len(grades[id]['questionscorrect'])):
				response_list.append((id,item,grades[id]['questionscorrect'][item]))
			item_param,user_param = irt(response_list)
		i=1
		for item,parameter in item_param.iteritems():
			g.write("Q%s,%s,%s\r\n" % (i,parameter['alpha'],parameter['beta']))
			i+=1

