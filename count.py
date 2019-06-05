import json
import string
from bs4 import BeautifulSoup
def count(obj,total,index):
	#build up inverted file
	try:
		for data in obj['contents']:
			if(data is None):
				continue
			if('subtype' in data):
				data['content'] = data['content'].lower()
			
				soup = BeautifulSoup(data['content'], 'html.parser')
				qq = soup.text
				temp = ''	
				for w in qq:
					if(w in string.punctuation):
						temp += ' '
					temp += w
				
					if(w in string.punctuation):
						temp += ' '
				for w in temp.split():
					if(len(w)):
						try:
							total[w] += 1
						except:
							total[w] = 1
	except Exception as e:
		print(index,obj)
		print(e)

total = {}
with open('./WashingtonPost.v2/data/TREC_Washington_Post_collection.v2.jl', 'r') as f:
	for i,line in enumerate(f):
		obj = json.loads(line)
		count(obj,total,i)

arr = [(key,total[key]) for key in total]
arr = sorted(arr,key= lambda x:x[1],reverse=True)

with open('./analysis/vocab','w') as f:
	for data in arr:
		f.write("{0}\t{1}\n".format(data[0],data[1]))
