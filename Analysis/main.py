import datetime
import json
import re
from FbDateParser import FbDateParser
import pandas as pd

INPUT_NAME = 'output_facebook_false.json'
fbdp = FbDateParser()

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def clean_text(text):                                                                                                      
    new_text = text.replace(',',' ')                                                                                        
    new_text = text.replace('\n',' ')  
    return re.sub(r'[^A-Za-z0-9 ]+', '', new_text)                                                                                       

with open(INPUT_NAME) as json_file:                                                                                         
    data = json.load(json_file)
    cp_data = []
    
    for item in data:
        item['facebok_date_parsed'] = fbdp.parse(item['facebook_date'], item['date'])
        reactions = item['reactions']

        item["all_reactions"] = int(reactions['all'])
        item["likes"] = int(reactions['likes'])
        item["love"] = int(reactions['love'])
        item["wow"] = int(reactions['wow'])
        item["haha"] = int(reactions['haha'])
        item["sad"] = int(reactions['sad'])
        item["angry"] = int(reactions['angry'])
        item["care"] = int(reactions['care'])
        item["content"] = clean_text(item["content"])
        item["author"] = clean_text(item["author"])
        item = removekey(item, 'reactions')
        cp_data.append(item)
    
    df = pd.DataFrame.from_dict(cp_data)
    df.to_csv('output_facebook_false_1.csv')
    print(df.head())