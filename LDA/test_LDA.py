import csv, random, time, sys, json
import numpy as np
import gensim
from gensim.utils import simple_preprocess
from gensim import corpora, models
from pprint import pprint
from gensim.test.utils import datapath
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer

# python test_LDA.py [all document filename] [query document filename] [LDA model]
# python test_LDA.py title_all.csv filelist lda_model_25c_all

num_topics = 25

def lemmatize_stemming(text):
	stemmer = SnowballStemmer("english")
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
def preprocess(text):
	result = []
	for token in gensim.utils.simple_preprocess(text):
		if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
			result.append(lemmatize_stemming(token))
	return result

data = []
index = dict()
with open(sys.argv[1], newline='') as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		data.append(row[2:])
		index[int(row[0])] = row[1]

print("Build dictionary.")
dictionary = gensim.corpora.Dictionary(data)
dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
bow_corpus = [dictionary.doc2bow(doc) for doc in data]

bow_corpus_pair = []
cn = 0
for item in bow_corpus:
	bow_corpus_pair.append((cn, item))
	cn += 1
"""
print("Run TFIDF model.")
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

print("Run LDA model.")
lda_model_tfidf = models.LdaMulticore(corpus_tfidf, num_topics=num_topics, id2word=dictionary, passes=2, workers=4)
for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

print("Save model to disk.")
temp_file = "lda_model_50c_all"
lda_model_tfidf.save(temp_file)"""

lda_model_tfidf = models.LdaMulticore.load(sys.argv[3], mmap='r')

print("Get vector of documents.")
tra_vec = []
for tra_data in bow_corpus_pair:
	tra_vec_tmp = lda_model_tfidf[tra_data[1]]
	tmp = []
	for c in range(0, num_topics):
		tmp.append(0)
	for i in tra_vec_tmp:
		tmp[i[0]] = i[1]
	tra_vec.append((tra_data[0], tmp))
	
print("Start testing.")
test_document = []
with open(sys.argv[2], 'r') as f:
	for line in f.readlines():
		line = line.strip('\n')
		print(line)
		file = open(line,'r')
		for li in file.readlines():
			obj = json.loads(li)
			tmp = []
			if obj['title'] == None:
				for a in preprocess(obj['text']):
					tmp.append(a)
			else:
				for a in preprocess(obj['title']):
					tmp.append(a)
				for a in preprocess(obj['text']):
					tmp.append(a)
			test_document.append((obj['id'] ,tmp))

test_dic = []
for item in test_document:
	tmp = []
	for word in item[1]:
		tmp.append(word)
	test_dic.append(tmp)

dictionary_test = gensim.corpora.Dictionary(test_dic)
dictionary_test.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
bow_corpus_test = [dictionary.doc2bow(doc) for doc in test_dic]
bow_corpus_pair_test = []
cn = 0
for item in bow_corpus_test:
	bow_corpus_pair_test.append((test_document[cn][0], item))
	cn += 1

for test_doc in bow_corpus_pair_test:
	test_tmp = lda_model_tfidf[test_doc[1]]
	test_vec = []
	for c in range(0, num_topics):
		test_vec.append(0)
	for i in test_tmp:
		test_vec[i[0]] = i[1]

	# calculate similarity
	score_all = []
	for item in tra_vec:
		score = np.dot(test_vec, item[1])
		score_all.append((index[item[0]], score))

	output_name = test_doc[0]+'.txt'
	f_out = open(output_name,'w')
	for i, s in score_all:
		f_out.write(str(i)+":"+str(s)+"\n")

f_out.close()



