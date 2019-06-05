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
				local = {}
				for w in temp.split():
					if(len(w)):
						try:
							local[w] += 1
						except:
							local[w] = 1
				for w in local:
					try:
						total[w]['docs'][index] = local[w]
					except:
						total[w] = {}
						total[w]['docs'] = {index:local[w]}
		return total
	except Exception as e:
		print(index,obj)
		print(e)

total = {}
with open('./WashingtonPost.v2/data/TREC_Washington_Post_collection.v2.jl', 'r') as f:
	for i,line in enumerate(f):
		obj = json.loads(line)
		total = count(obj,total,i)
with open('./invertedq.json', 'w') as f:
	f.write(json.dumps(total))
