import json
import pandas as pd
from urllib.parse import urlparse

poynter = pd.read_csv('./dataset/poynter.csv')
filtered = []

def check_url(url):
    res = False
    for index, item in poynter.iterrows():
        a_url = str(item['checked_link'])
        b_url = str(url)
        
        if(a_url == b_url):
            res = True
            break
    
    return res

with open('./dataset/data_feed.json') as json_file:
    data = json.load(json_file)
    data = data['dataFeedElement']
    prog = 0
    print(len(data))

    for google in data:
        try:
            google_item = google["item"][0]
            if(check_url(google_item["url"])):
                filtered.append(google)
        except:
            pass
        
        if (prog % 5) == 0:
            print(filtered)
            with open('./dataset/google_covid_by_url_chunk.json', 'w') as outfile:
                json.dump(filtered, outfile)
            outfile.close()
        
        prog = prog + 1
        print(str(prog)+'/'+str(len(data)))

json_file.close()