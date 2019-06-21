import os
import sys
import json

check = 'Extracted the following NER entity mentions:'

filelist = list(os.listdir('./NER/'))

data = {}
for filename in filelist:
	count = set()
	with open('./NER/{0}'.format(filename)) as f:
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
	base = filename.split('.')[0]
	for line in count:
		try:
			data[line].append(base)
		except:
			data[line] = [ base ]
json.dump(data,open('./ner_inverted.json','w'))
