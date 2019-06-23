import json, sys
import string
from bs4 import BeautifulSoup
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2019)
import nltk
nltk.download('wordnet')

# python extract.py [input filename] [output filename]
# python extract.py /public/TREC/WashingtonPost.v2/data/TREC_Washington_Post_collection.v2.jl title_all.csv

def lemmatize_stemming(text):
	stemmer = SnowballStemmer("english")
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
def preprocess(text):
	result = []
	for token in gensim.utils.simple_preprocess(text):
		if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
			result.append(lemmatize_stemming(token))
	return result
def text(obj):
	result = []
	try:
		for data in obj['contents']:
			if(data is None):
				continue
			if('subtype' in data):
				data['content'] = data['content'].lower()
			
				soup = BeautifulSoup(data['content'], 'html.parser')
				if soup.text != None:
					result.append(preprocess(soup.text))
	except Exception as e:
		print(index,obj)
		print(e)
	total = []
	for item in result:
		for par in item:
			total.append(par)
	return total

f_out = open(sys.argv[2],'w')

with open(sys.argv[1], 'r') as f:
	for i,line in enumerate(f):
		obj = json.loads(line)
		tmp = []
		if obj['title'] == None:
			tmp.append(str(i))
			tmp.append(obj['id'])
			for a in text(obj):
				tmp.append(a)
			f_out.write(','.join(tmp))
			f_out.write("\n")
		else:
			tmp.append(str(i))
			tmp.append(obj['id'])
			for a in preprocess(obj['title']):
				tmp.append(a)
			for a in text(obj):
				tmp.append(a)
			f_out.write(','.join(tmp))
			f_out.write("\n")



