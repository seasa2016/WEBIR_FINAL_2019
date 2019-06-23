import json
import subprocess
import os
import operator

class GRAPH:
    def __init__(self,config,model):
        self.model = model
        self.config = config
        
        self.init()
    def init(self):
        # create inverted file for the name entity
        self.ner_inverted = json.load(open(self.config.ner_inverted))
        self.mapping = {}
        with open(self.config.mapping) as f:
            for line in f:
                line = line.split()
                self.mapping[line[1]] = line[0]

    def parsing_ner(self,ner_file):
        ners = []
        with open(ner_file) as f:
            for line in f:
                line = line.strip().split()
                ners.append(line)
        return ners

    def rank(self,input_dir):
        #check the name entity
        similarity_scores = self.model.find( query_list=os.path.join(input_dir,'input_file'), num_retrieve=0 )
        ners = self.parsing_ner( os.path.join(input_dir,'query') )

        rank = []
        for i,(ner, query) in enumerate(zip(ners,similarity_scores)):
            qid, text_score = query
            ner_score = {}
                        
            for n in ner:
                if(n in self.ner_inverted):
                    ner_score[n] = 0
                    count = 0
                    for text_id in self.ner_inverted[n]:
                        try:
                            ner_score[n] += text_score[ self.mapping[text_id] ]
                            count += 1
                        except:
                            pass
                    ner_score[n] /= count
            # rank n
            rank.append( (qid, sorted(ner_score.items(),key=operator.itemgetter(1), reverse=True) ))

        return rank     
