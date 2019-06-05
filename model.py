import json
import math
import sys

with open(sys.argv[1]) as f:
	for line in f:
		pass

data = json.loads(line)
length = {}

for i,key in enumerate(data):
	for doc,doc_tf in data[key]['docs'].items():
		try:
			length[doc] += doc_tf
		except:
			length[doc] = doc_tf
		
total = 0
for doc in length:
	total += length[doc]
length['avg'] = total/len(length)
with open('./model/doc_length.json','w') as f:
	f.write(json.dumps(length))

l = len(data)
for i,key in enumerate(data):
	data[key]['idf'] = math.log(l/len(data[key]['docs']),2)
with open('./model/inverted_file_idf.json','w') as f:
	f.write(json.dumps(data))

l = len(data)
for i,key in enumerate(data):
	data[key]['idf'] = max(0,math.log((l-len(data[key]['docs']))/len(data[key]['docs']),2))
with open('./model/inverted_file_prob_idf.json','w') as f:
	f.write(json.dumps(data))























