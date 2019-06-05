import json
import pandas as pd
import numpy as np
import random
import csv
import operator
from argparse import ArgumentParser
from collections import Counter
import math

parser = ArgumentParser()
parser.add_argument("-i", "--inverted_file", default='./model/inverted_file.json', dest = "inverted_file", help = "Pass in a .json file.")
parser.add_argument("-l", "--doc_length", default='./model/doc_length.json', dest = "doc_length", help = "Pass in a .json file.")
parser.add_argument("-d", "--doc_file", default='./model/document_file_log_tf.json', dest = "doc_file", help = "Pass in a .json file.")
parser.add_argument("-q", "--query_file", default='QS_1.csv', dest = "query_file", help = "Pass in a .csv file.")
parser.add_argument("-c", "--corpus_file", default='NC_1.csv', dest = "corpus_file", help = "Pass in a .csv file.")
parser.add_argument("-o", "--output_file", default='sample_output.csv', dest = "output_file", help = "Pass in a .csv file.")
parser.add_argument("-k1", "--okapi_k1", default=15,type=float, dest = "k1", help = "parameter for okapi")
parser.add_argument("-k3", "--okapi_k3", default=15,type=float, dest = "k3", help = "parameter for okapi")
parser.add_argument("-b", "--okapi_b", default=7,type=float, dest = "b", help = "parameter for okapi")

parser.add_argument("-alpha", "--feedback_alpha", default=8,type=float, dest = "alpha", help = "feedback alpha")
parser.add_argument("-num", "--feedback_num", default=10,type=int, dest = "num", help = "feedback num")

args = parser.parse_args()

k1 = args.k1/10
k3 = args.k3/10
b = args.b/10
args.feedback=True

num=args.num
alpha =args.alpha/num/10

# load inverted file
with open(args.inverted_file) as f:
	invert_file = json.load(f)
with open(args.doc_length) as f:
	doc_length = json.load(f)
	l_avg = doc_length['avg']

if(args.feedback):
	with open(args.doc_file) as f:
		doc_file = json.load(f)

# read query and news corpus
querys = np.array(pd.read_csv(args.query_file)) # [(query_id, query), (query_id, query) ...]
corpus = np.array(pd.read_csv(args.corpus_file)) # [(news_id, url), (news_id, url) ...]
num_corpus = corpus.shape[0] # used for random sample

# process each query
final_ans = []
total = dict()

for word in invert_file:
	doc_idf = invert_file[word]['idf']
	for document_count_dict in invert_file[word]['docs']:
		for doc, doc_tf in document_count_dict.items():
			doc_tf = math.log(doc_tf,2) + 1
			try:
				total[doc] += (doc_tf * doc_idf)**2
			except:
				total[doc] = (doc_tf * doc_idf)**2

for (query_id, query) in querys:
	print("query_id: {}".format(query_id))
	 
	# counting query term frequency
	query_cnt = Counter()
	query_words = list(jieba.cut(query))
	query_cnt.update(query_words)

	# calculate scores by tf-idf
	document_scores = dict() # record candidate document and its scores
	for (word, count) in query_cnt.items():
		if word in invert_file:
			query_tf = 1
			#query_tf = count
			query_tf = 1 + math.log(count,2)
			#query_tf = (k3+1)*count/(k3+count)
			
			query_idf = invert_file[word]['idf']
			doc_idf = invert_file[word]['idf']
			#doc_idf = 1

			for document_count_dict in invert_file[word]['docs']:
				for doc, doc_tf in document_count_dict.items():
					doc_tf = math.log(doc_tf,2) + 1
					#doc_tf = (k1+1)*doc_tf/( k1*((1-b) + b*(doc_length[doc]/l_avg)) + doc_tf)

					try:
						document_scores[doc] += query_tf * query_idf * doc_tf * doc_idf
					except:
						document_scores[doc] = query_tf * query_idf * doc_tf * doc_idf
					
	
	# sort the document score pair by the score
	scores_temp = {}
	for key in document_scores:
		scores_temp[key] = document_scores[key] / math.sqrt(total[key])
	sorted_document_scores = sorted(scores_temp.items(), key=operator.itemgetter(1), reverse=True)
	
	#do the feedback here
	if(args.feedback):
		expand = {}
		for doc_score_tuple in sorted_document_scores[:num]:
			for word,count in doc_file[ doc_score_tuple[0] ].items():
				try:
					expand[word] += count
				except:
					expand[word] = count

		for (word, count) in expand.items():
			if word in invert_file:
				#query_tf = 1
				#query_tf = count
				query_tf = 1 + math.log(count,2)
				#query_tf = (k3+1)*count/(k3+count)
				
				query_idf = invert_file[word]['idf']
				doc_idf = invert_file[word]['idf']
				#doc_idf = 1

				for document_count_dict in invert_file[word]['docs']:
					for doc, doc_tf in document_count_dict.items():
						doc_tf = math.log(doc_tf,2) + 1
						#doc_tf = (k1+1)*doc_tf/( k1*((1-b) + b*(doc_length[doc]/l_avg)) + doc_tf)
						try:
							document_scores[doc] += alpha*query_tf * query_idf * doc_tf * doc_idf
						except:
							document_scores[doc] = alpha*query_tf * query_idf * doc_tf * doc_idf
		scores_temp = {}
		for key in document_scores:
			scores_temp[key] = document_scores[key] / math.sqrt(total[key])
		sorted_document_scores = sorted(scores_temp.items(), key=operator.itemgetter(1), reverse=True)

	# record the answer of this query to final_ans
	if len(sorted_document_scores) >= 300:
		final_ans.append([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores[:300]])
	else: # if candidate documents less than 300, random sample some documents that are not in candidate list
		documents_set  = set([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores])
		sample_pool = ['news_%06d'%news_id for news_id in range(1, num_corpus+1) if 'news_%06d'%news_id not in documents_set]
		sample_ans = random.sample(sample_pool, 300-count)
		sorted_document_scores.extend(sample_ans)
		final_ans.append([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores])
	
# write answer to csv file
with open(args.output_file, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	head = ['Query_Index'] + ['Rank_%03d'%i for i in range(1,301)]
	writer.writerow(head)
	for query_id, ans in enumerate(final_ans, 1):
		writer.writerow(['q_%02d'%query_id]+ans)
