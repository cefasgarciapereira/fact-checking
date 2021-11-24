import pandas as pd

def isNaN(string):
    return string != string

def listBrokenUrls():
    #declaration of variables
    i = 1
    broken_urls = []

    #reading file
    df = pd.read_csv("poynter_all.csv")
    urls = df['checked_link']

    #iterating over files
    for url in urls:
        i = i + 1
        if(isNaN(url)):
            broken_urls.append(i)

    print(str(len(broken_urls))+' links corrompidos: \n')
    for url in broken_urls:
        print(url)

def filterTweetsId(twitter_id):
    twitter_id_filter = ["tweet", "", "compose"]
    valid = True

    for id_filter in twitter_id_filter:
        if(twitter_id == id_filter):
            valid = False
    return valid

print(filterTweetsId('tweet'))