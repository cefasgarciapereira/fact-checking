import json
from datetime import datetime
filtered = []

def check_covid(text):
    covid_terms = [
        'covid',
        'corona',
        'sars',
        'pfizer',
        'astrazeneca',
        'outbreak',
        'cov2',
        'ncov',
        '2019nCoV',
        'coronavirus outbreak',
        'pandemi',
        'china virus',
        'wuhan virus',
    ]

    for word in covid_terms:
        if(word in str(text)):
            return True
    return False


def valid_date(date):
    f = '%Y-%m-%d'
    start_date = datetime.strptime("2020-01-01", f)
    end_date = datetime.strptime("2021-01-01", f)   
    current_date = datetime.strptime(date, f) 
    
    if(start_date <= current_date <= end_date):
        return True
    
    return False

with open('./dataset/data_feed.json') as json_file:
    data = json.load(json_file)
    data = data['dataFeedElement']
    prog = 0
    print(len(data))

    for google in data:
        try:
            google_item = google["item"][0]
            if(check_covid(google_item["claimReviewed"]) or check_covid(google_item["url"])):
                filtered.append(google)
        except:
            pass

        prog = prog + 1
        print(str(prog)+'/'+str(len(data)))

with open('./dataset/google_covid_all.json', 'w') as outfile:
    json.dump(filtered, outfile)
