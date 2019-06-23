from VSM.retrieval import VSM
from graph.graph import GRAPH
from argparse import ArgumentParser



def main(args):
	print('build vsm model')
	vsm_model = VSM(args)
	print('build graph model')
	model = GRAPH(args,vsm_model)

	print('do ranking')
	outs = model.rank(args.query_file)
	
	with open(args.output_file,'w') as f:
		for out in outs:
			f.write("{0}\t{1}\n".format(out[0],out[1]))

if(__name__ == "__main__"):
	parser = ArgumentParser()
	parser.add_argument("-q", "--query_dir", default='./input/', dest = "query_file", help = "Pass in a .csv file.")
	parser.add_argument("-o", "--output_file", default='sample_output.csv', dest = "output_file", help = "Pass in a .csv file.")

    # parameter for similarity model
	parser.add_argument("-i", "--inverted_file", default='./VSM/model/inverted_file_idf.json', dest = "inverted_file", help = "Pass in a .json file.")
	parser.add_argument("-l", "--doc_length", default='./VSM/model/doc_length.json', dest = "doc_length", help = "Pass in a .json file.")
	parser.add_argument("-d", "--doc_file", default='./VSM/model/document_file_log_tf.json', dest = "doc_file", help = "Pass in a .json file.")

    #parameter for graph model
	parser.add_argument("-n", "--ner_file", default='./ner_inverted.json', dest = "ner_inverted", help = "Pass in a .json file.")

    
	args = parser.parse_args()
	args.feedback = False
	args.alpha = 0.8
	args.num = 10

	main(args)
