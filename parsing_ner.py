import os
import sys
import json
import glob

database = True
if(len(sys.argv)==3 and sys.argv[2]=='query'):
	database = False

check = 'Extracted the following NER entity mentions:'

filelist = glob.glob( '{0}/*.out'.format(sys.argv[1]))

ners = []
data = {}
for filename in filelist:
	count = set()
	with open(filename) as f:
		lines = f.readlines()
		i=0
		while(i < len(lines)):
			if(lines[i][:len(check)]==check):
				i+=1
				while(i<len(lines) and lines[i]!='\n'):
					ner = lines[i].strip().split()
					
					if(ner[0][:4]=='http'):
						i+=1
						continue

					ner = ' '.join(ner[:-1])
					count.add(ner)
					i=i+1
			i=i+1
	ners.append(count)
	base = filename.split('.')[0].split('/')[-1]
	for line in count:
		try:
			data[line].append(base)
		except:
			data[line] = [ base ]
if(database):
	json.dump(data,open('./{0}/ner_inverted.json'.format(sys.argv[1]),'w'))
else:
	with open('./{0}/query'.format(sys.argv[1]),'w') as f:
		for ner in ners:
			f.write('\t'.join(ner))
			f.write('\n')
			

# Get inverse doc freq. of entities
import numpy as np

ner_inverted = json.load(open('ner_inverted.json'))
entities = list(ner_inverted.keys())

ent_len = dict()
N = 595000   # number of docs in the collection
for ent in entities:
	_df = len(ner_inverted[ent])
	ent_len[ent] = np.log10( N/_df)
	
with open('entity_idf.json', 'w') as json_file: 
	json.dump(ent_len, json_file)
