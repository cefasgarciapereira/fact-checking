import json
import numpy as np
import pandas as pd

dates = []

with open('./dataset/google_covid.json') as json_file:
    data = json.load(json_file)
    data = data
    print(len(data))

    for register in data:
        item = register["item"][0]
        try:
            dates.append({
            "url": str(register["url"]),
            "date": str(register["dateModified"])[0:10]
            })
        except:
            try:
                dates.append({
                "url": str(register["url"]),
                "date": str(register["dateCreated"])[0:10]
                })
            except:
                try:
                    dates.append({
                        "url": str(register["url"]),
                        "date": item["itemReviewed"]["datePublished"]
                    })
                except:
                    pass

dataframe = pd.DataFrame(dates) 
dataframe.to_csv('./dataset/google_covid_dates_by_url_2.csv')
