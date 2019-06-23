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
			

