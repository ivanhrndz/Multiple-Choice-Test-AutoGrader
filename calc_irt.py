from pyirt._pyirt import irt
import numpy as np
grades = np.loadtxt("simulated.csv",delimiter=",",dtype=np.int)
response_list=[]
for user in range(grades.shape[0]):
	for item in range(grades.shape[1]):
		response_list.append((user,item,grades[user,item]))
item_param,user_param = irt(response_list)