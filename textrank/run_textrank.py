import pytextrank
import sys
import pandas as pd
import json
import numpy as np

in_files = []   # file name for json files
with open('input/filelist') as f:
    for line in f:
        line = line.replace('\n', '')
        in_files.append(line)

def _get_keywords(path_stage0, path_stage2):
    # Stage 1: parse doc
    path_stage1 = 'o1.json'
    with open(path_stage1, 'w') as f:
        for graf in pytextrank.parse_doc(pytextrank.json_iter(path_stage0)):
            f.write("%s\n" % pytextrank.pretty_print(graf._asdict()))

    # Stage 2: rank words
    graph, ranks = pytextrank.text_rank(path_stage1)
    pytextrank.render_ranks(graph, ranks)

    result_dict = dict()
    with open(path_stage2, 'w') as f2:
        for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
            _ro = rl._asdict()
            ro = dict()
            ro[ _ro['text'] ] = _ro['rank']
            #f2.write("%s\n" % pytextrank.pretty_print(ro))
            
            result_dict[ _ro['text'] ] = _ro['rank']

    return result_dict

def _rank_entities(entities, result_dict, entity_idf, w_tr=400, w_idf=1):
    # result_dict: from textrank  (value: 0.03...)
    # entity_idf: idf  (value: max=5.77...)
    # weights: w_tr (textrank), w_idf (idf)
    ent_score = []
    for ent in entities:
        if ent in result_dict.keys() and ent in entity_idf.keys():
            score_textrank = result_dict[ent]
            score_idf = entity_idf[ent]
            score_total = score_textrank*w_tr + score_idf*w_idf
            ent_score.append((ent, score_total ))
        elif ent in entity_idf.keys():
            ent_score.append((ent, entity_idf[ent]*w_idf))
        else:
            ent_score.append((ent, 0))
    ent_score.sort(key=lambda tup:tup[1], reverse=True)

    return ent_score

import time
start = time.time()

# Load entities
doc2entity = json.load(open('doc2entity.json'))
entity_idf = json.load(open('entity_idf.json'))

for f_in in in_files:
    path_stage0 = f_in
    doc_id = f_in.split('/')[1]
    doc_id = doc_id.split('.')[0]
    #path_stage2 = 'result_input/'+str(doc_id)+'.txt'
    path_stage2 = 'o2.json'
    print(doc_id)

    result_dict = _get_keywords(str(path_stage0), str(path_stage2))
    entities = doc2entity[doc_id]

    ent_score = _rank_entities(entities, result_dict, entity_idf)

    df = pd.DataFrame(ent_score)
    df.to_csv('result_input/'+str(doc_id)+'.txt', header=None)

print ('time: ', time.time()-start)

'''
# Visualize result

import networkx as nx
import matplotlib.pylab as plt

nx.draw(graph, with_labels=True) 
plt.savefig('view_result.png')
'''
