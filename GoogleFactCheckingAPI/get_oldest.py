import json
from datetime import datetime

min_date = datetime.strptime('2021-09-01', '%Y-%m-%d')
oldest_item = False

def check_covid(text):
    covid_terms = [
        'covid',
        'corona',
        'sars',
        'pfizer',
        'astrazeneca',
        'bill gates',
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
    start_date = datetime.strptime("2019-12-01", f)
    end_date = datetime.strptime("2021-01-01", f)   
    current_date = date
    
    if(start_date <= current_date <= end_date):
        return True
    
    return False

def get_min_date(date, item):
    global min_date    
    f = '%Y-%m-%d'
    current_date = datetime.strptime(date, f) 
    
    if(current_date < min_date):
        if(valid_date(current_date) and (check_covid(item["claimReviewed"]) or check_covid(item["url"]))):
            min_date = current_date
            return True

    return False

with open('./dataset/google_covid.json') as json_file:
    data = json.load(json_file)
    prog = 0
    print(len(data))

    for register in data:
        item = register["item"][0]
        try:
            if(get_min_date(str(register["dateModified"][0:10]), item)):
                oldest_item = item
        except:
            try:
                if(get_min_date(str(register["dateCreated"][0:10]), item)):
                    oldest_item = item
            except:
                try:
                    if(get_min_date(str(item["itemReviewed"]["datePublished"]), item)):
                        oldest_item = item
                except:
                    pass
        prog = prog + 1
        print(prog)

print("Min Date: ", min_date)
print(oldest_item)