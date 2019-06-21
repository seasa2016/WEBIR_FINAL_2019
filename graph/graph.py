import json

class GRAPH:
    def __init__(self,config,model):
        self.model = model
        self.config = config
    def init(self):
        # create inverted file for the name entity
        self.ner_inverted = json.load(open(self.config.ner_inverted))
    
    def rank(self,querys):
        