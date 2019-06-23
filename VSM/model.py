import json
import math
import sys

data = json.load(open(sys.argv[1]))
length = {}
total = {}

for i,key in enumerate(data):
	for doc,doc_tf in data[key]['docs'].items():
		try:
			length[doc] += doc_tf
		except:
			length[doc] = doc_tf

		if(doc in total):
			total[doc][key] = doc_tf
		else:
			total[doc] = {}
			total[doc][key] = doc_tf

with open('./model/document_file_log_tf.json','w') as f:
	f.write(json.dumps(total))
		
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























