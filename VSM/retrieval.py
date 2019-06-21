import json
import pandas as pd
import numpy as np
import random
import csv
import operator
from argparse import ArgumentParser
from collections import Counter
import math

class VSM:
	def __init__(self,args):
		# initial argument

		#for okapi
		self.k1 = args.k1
		self.k3 = args.k3
		self.b = args.b
		#for tfidf
		self.feedback = args.feedback
		self.alpha = args.alpha
		self.num = args.num

		# load inverted file
		with open(args.inverted_file) as f:
			self.invert_file = json.load(f)
			self.total = {}
			for word in self.invert_file:
				doc_idf = self.invert_file[word]['idf']
				for doc, doc_tf in self.invert_file[word]['docs'].items():
					doc_tf = math.log(doc_tf,2) + 1
					try:
						self.total[doc] += (doc_tf * doc_idf)**2
					except:
						self.total[doc] = (doc_tf * doc_idf)**2

		with open(args.doc_length) as f:
			self.doc_length = json.load(f)
			#self.l_avg = self.doc_length['avg']

		if(self.feedback):
			with open(args.doc_file) as f:
				self.doc_file = json.load(f)



	def parsing(self,query_file):
		mispell_dict = {'didnt':'did not','doesnt':'does not',
                'isnt':'is not','shouldnt':'should not' ,
                'wasnt': 'was not' ,'hasnt': 'has not' ,
                '‘i': 'i' ,'theatre': 'theater' ,'cancelled': 'canceled' ,
                'organisation': 'organization' ,'labour': 'labor' ,
                'favourite': 'favorite' ,'travelling': 'traveling' ,'washingtons': 'washington' ,
                'marylands': 'maryland' ,'chinas': 'china' ,'russias': 'russia' ,
                '‘the': 'the' ,'irans': 'iran','dulles': 'dulle' 
                }
		query_data = []
		with open(query_file) as f:
			for line in f:
				qid,text = line.split('\t')
				total = {}

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
						total[w] += 1
					except:
						total[w] = 1

				query_data.append((qid,total))
		return query_data

	def find(self,query_file):
		def count(document_scores,query):
			for (word, count) in query.items():
				if word in self.invert_file:
					#query_tf = 1
					#query_tf = count
					query_tf = 1 + math.log(count,2)
					#query_tf = (k3+1)*count/(k3+count)
					
					query_idf = self.invert_file[word]['idf']
					doc_idf = self.invert_file[word]['idf']
					#doc_idf = 1

					for doc, doc_tf in self.invert_file[word]['docs'].items():
						doc_tf = math.log(doc_tf,2) + 1
						#doc_tf = (k1+1)*doc_tf/( k1*((1-b) + b*(doc_length[doc]/l_avg)) + doc_tf)
						try:
							document_scores[doc] += query_tf * query_idf * doc_tf * doc_idf
						except:
							document_scores[doc] = query_tf * query_idf * doc_tf * doc_idf


		querys = self.parsing(query_file)

		final_ans = []
		for i,(query_id, query) in enumerate(querys):
			print("query_id: {}".format(query_id))
		
			# calculate scores by tf-idf
			document_scores = dict() # record candidate document and its scores
			count(document_scores,query)
							
			
			# sort the document score pair by the score
			scores_temp = {}
			for key in document_scores:
				scores_temp[key] = document_scores[key] / math.sqrt(self.total[key])
			sorted_document_scores = sorted(scores_temp.items(), key=operator.itemgetter(1), reverse=True)
			
			#do the feedback here
			if(args.feedback):
				expand = {}
				for doc_score_tuple in sorted_document_scores[:self.num]:
					for word,count in self.doc_file[ doc_score_tuple[0] ].items():
						try:
							expand[word] += count
						except:
							expand[word] = count

				count(document_scores,expand)

				scores_temp = {}
				for key in document_scores:
					scores_temp[key] = document_scores[key] / math.sqrt(self.total[key])
				sorted_document_scores = sorted(scores_temp.items(), key=operator.itemgetter(1), reverse=True)

			# record the answer of this query to final_ans
			if len(sorted_document_scores) >= 300:
				final_ans.append([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores[:300]])
			else: # if candidate documents less than 300, random sample some documents that are not in candidate list
				documents_set  = set([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores])
				sample_pool = ['news_%06d'%news_id for news_id in range(1, 300) if 'news_%06d'%news_id not in documents_set]
				sample_ans = random.sample(sample_pool, 300-count)
				sorted_document_scores.extend(sample_ans)
				final_ans.append([doc_score_tuple[0] for doc_score_tuple in sorted_document_scores])
		return final_ans

	def output(self,output_file,final_ans):
		# write answer to csv file
		with open(output_file, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			head = ['Query_Index'] + ['Rank_%03d'%i for i in range(1,301)]
			writer.writerow(head)
			for query_id, ans in enumerate(final_ans, 1):
				writer.writerow(['q_%02d'%query_id]+ans)

def main(args):
	# do the initial
	args.feedback=False
	args.alpha =args.alpha/args.num/10

	model = VSM(args)
	ans = model.find(args.query_file)
	model.output(args.output_file,ans)

if(__name__ == "__main__"):
	parser = ArgumentParser()
	parser.add_argument("-i", "--inverted_file", default='./model/inverted_file_idf.json', dest = "inverted_file", help = "Pass in a .json file.")
	parser.add_argument("-l", "--doc_length", default='./model/doc_length.json', dest = "doc_length", help = "Pass in a .json file.")
	parser.add_argument("-d", "--doc_file", default='./model/document_file_log_tf.json', dest = "doc_file", help = "Pass in a .json file.")
	parser.add_argument("-q", "--query_file", default='./train', dest = "query_file", help = "Pass in a .csv file.")
	parser.add_argument("-o", "--output_file", default='sample_output.csv', dest = "output_file", help = "Pass in a .csv file.")
	parser.add_argument("-k1", "--okapi_k1", default=15,type=float, dest = "k1", help = "parameter for okapi")
	parser.add_argument("-k3", "--okapi_k3", default=15,type=float, dest = "k3", help = "parameter for okapi")
	parser.add_argument("-b", "--okapi_b", default=7,type=float, dest = "b", help = "parameter for okapi")

	parser.add_argument("-alpha", "--feedback_alpha", default=8,type=float, dest = "alpha", help = "feedback alpha")
	parser.add_argument("-num", "--feedback_num", default=10,type=int, dest = "num", help = "feedback num")

	args = parser.parse_args()
	main(args)
