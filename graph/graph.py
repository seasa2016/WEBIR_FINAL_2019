import json
import subprocess
import os
import operator

class GRAPH:
    def __init__(self,config,model):
        self.model = model
        self.config = config

        self.input_dir = config.input_dir
        

    def init(self):
        # create inverted file for the name entity
        self.ner_inverted = json.load(open(self.config.ner_inverted))
    
    def parsing_ner(self,ner_file):
        ners = []
        with open(ner_file) as f:
            for line in f:
                line = line.strip().split()
                ners.append(line)
        return ners

    def rank(self,query_dir):
        #check the name entity
        querys = self.model.parsing( os.path.join(self.input_dir,'input_file') )
        ners = self.parsing_ner( os.path.join(self.input_dir,'query') )

        rank = []

        for i,(ner, query) in enumerate(zip(ners,querys)):
            qid, text = query
            ner_score = {}
            text_score = {}
            
            self.model.count(text_score, text)
            
            for n in ner:
                if(n in self.ner_inverted):
                    ner_score[n] = 0
                    for text_id in self.ner_inverted[n]:
                        ner_score[n] += text_score[text_id]
                    ner_score[n] /= len(self.ner_inverted[n])
            # rank n
            rank.append( (n, sorted(ner_score.items(),key=operator.itemgetter(1), reverse=True) ))

        return rank     
