import json
import string
from bs4 import BeautifulSoup
def parse(obj,index):
	#build up inverted file
	total = {}
	for key in ['id','article_url','title','author']:
		total[key] = obj[key]
	total['text'] = []
	try:
		for data in obj['contents']:
			if(data is None):
				continue
			if('subtype' in data):
				data['content'] = data['content'].lower()
			
				soup = BeautifulSoup(data['content'], 'html.parser')
				total['text'].append(soup.text)
	except Exception as e:
		print(index,obj)
		print(e)
	
	total['text'] = '\n'.join(total['text'])
	with open('./text/{0}.json'.format(obj['id']),'w') as f:
		f.write(json.dumps(total))

with open('./WashingtonPost.v2/data/TREC_Washington_Post_collection.v2.jl', 'r') as f:
	for i,line in enumerate(f):
		obj = json.loads(line)
		parse(obj,i)
	
