import json
import string
from bs4 import BeautifulSoup
def count(obj,index):
    #build up inverted file
    total = []
    for data in obj['contents']:
        if(data is None):
            continue
        if('subtype' in data):
            data['content'] = data['content'].lower()
        
            soup = BeautifulSoup(data['content'], 'html.parser')
            for i in soup.find_all('a'):
                total.append(i.text)
    return total

f_out = open('./model/entity.csv','w')
f_out.write("id,entity\n")

with open('./WashingtonPost.v2/data/TREC_Washington_Post_collection.v2.jl', 'r') as f:
    for i,line in enumerate(f):
        obj = json.loads(line)

        f_out.write("{0},{1}\n".format(obj['id'],count(obj,i)))

