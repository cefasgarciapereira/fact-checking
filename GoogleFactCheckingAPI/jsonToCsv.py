import json
import numpy as np
import pandas as pd

google_items = []

with open('./dataset/google_covid_all.json') as json_file:
    data = json.load(json_file)
    data = data
    prog = 0
    print(len(data))

    for register in data:
        item = register["item"][0]
        item_date = ''
        author_name = ''

        # get date
        try:
            item_date = str(register["dateModified"])[0:10]
        except:
            try:
                item_date=str(register["dateCreated"])[0:10]
            except:
                try:
                    item_date=item["itemReviewed"]["datePublished"]
                except:
                    pass
        
        # get author name
        try:
            author_name = item["author"]["name"]
        except:
            pass

        google_items.append({
            "claimReviewed": item["claimReviewed"],
            "datePublished": item_date,
            "author_name": author_name,
            "url": item["url"]
        })

        prog=prog + 1
        print(str(prog)+'/'+str(len(data)))

dataframe=pd.DataFrame(google_items)
dataframe.to_csv('./dataset/GoogleCovid.csv')
