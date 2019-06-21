"""
this file is used for clean up data
"""
import os
import sys
import json
import string
from bs4 import BeautifulSoup
import re

mispell_dict = {'didnt':'did not',
                'doesnt':'does not',
                'isnt':'is not',
                'shouldnt':'should not' ,
                'wasnt': 'was not' ,
                'hasnt': 'has not' ,
                '‘i': 'i' ,
                'theatre': 'theater' ,
                'cancelled': 'canceled' ,
                'organisation': 'organization' ,
                'labour': 'labor' ,
                'favourite': 'favorite' ,
                'travelling': 'traveling' ,
                'washingtons': 'washington' ,
                'marylands': 'maryland' ,
                'chinas': 'china' ,
                'russias': 'russia' ,
                '‘the': 'the' ,
                'irans': 'iran' ,
                'dulles': 'dulle' 
                }

def parse(text,vocab,total,index):
	#build up inverted file

	for punct in "/-'":
		text = text.replace(punct, '')
	for punct in '?!.,"#$%\'()*+-/:;<=>@[\\]^_`{|}~' + '“”’‘':
		text = text.replace(punct, '')
	"""
	if you want to parse number
	text = str(key)
	text = re.sub('[0-9]{5,}', '#####', text)
	text = re.sub('[0-9]{4}', '####', text)
	text = re.sub('[0-9]{3}', '###', text)
	text = re.sub('[0-9]{2}', '##', text)
	"""
	for key,data in mispell_dict.items():
		text = text.replace(key,data)
	
	for w in text.split():
		try:
			total[w]['docs'][index] += 1
		except KeyError as e:
			if(e.args[0]==w):
				total[w] = {}
				total[w]['docs'] = {index:1}
			elif(e.args[0] == index):
				total[w]['docs'][index] = 1


		try:
			vocab[w] += 1
		except:
			vocab[w] = 1

total = {}
vocab = {}
mapping = []

file_name = list(os.listdir('./../text/'))
for i,name in enumerate(file_name):
	with open(os.path.join('./../text/',name), 'r') as f:
		line =  f.readline()
		obj = json.loads(line)
		mapping.append((obj['id'],obj['article_url']))
		parse(obj['text'],vocab,total,i)
arr = [(key,data) for key,data in vocab.items()]
arr = sorted(arr,key=lambda x:x[1],reverse=True)
with open('./model/vocab','w') as f:
	for data in arr:
		f.write("{0}\t{1}\n".format(data[0],data[1]))

with open('./model/mapping','w') as f:
	for i,d in enumerate(mapping):
		f.write("{0}\t{1}\t{2}\n".format(i,d[0],d[1]))

with open('./model/inverted.json', 'w') as f:
	f.write(json.dumps(total))
