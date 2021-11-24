import tweepy
import csv
import pandas as pd
import math
import secrets
import json

INPUT_NAME = './poynter_social_false.json'
PROCESSED_IDS = 'tweet_output_false_bkp.csv'
FILE_NAME = 'tweet_output_false.csv'
ERROR_FILE = 'test_error.py'

def rc(value):
    #remove commas
    new_value = str(value).replace(',',' ')
    return new_value

def create_file():
    with open (FILE_NAME, 'a+', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['id', 'user_id','text', 'created_at', 'geo', 'place_name', 'coordinates', 'user_location', 'likes', 'retweets', 'followers', 'lang'])

def extract_ids_from_file_deprecated():
    twitter_posts = pd.read_csv(INPUT_NAME)
    twitter_ids = twitter_posts.filter(regex='^twitter_ids',axis=1)
    values=[]
    ids=[]
    errors = 0
    posts = 0

    for value in twitter_ids.values.tolist():
        values += value

    for value in values:
        try:
            str_value = str(value)
            str_value = str_value.replace('_','')
            if((not math.isnan(float(str_value))) and (len(str(str_value)) > 5)):
                posts = posts+1
                ids.append(str(str_value))
        except:
            errors = errors + 1
            pass
    print('--- Extraction ---')
    print('Total values: '+str(errors+posts))
    print('Errors: '+str(errors))
    print('Post IDs: '+str(posts))
    print('------------------\n')
    return ids

def extract_ids_from_file_deprecated():
    twitter_posts = pd.read_csv(INPUT_NAME)
    twitter_ids = twitter_posts.filter(regex='^twitter_ids',axis=1)
    values=[]
    ids=[]
    errors = 0
    posts = 0

    for value in twitter_ids.values.tolist():
        values += value

    for value in values:
        try:
            str_value = str(value)
            str_value = str_value.replace('_','')
            if((not math.isnan(float(str_value))) and (len(str(str_value)) > 5)):
                posts = posts+1
                ids.append(str(str_value))
        except:
            errors = errors + 1
            pass
    print('--- Extraction ---')
    print('Total values: '+str(errors+posts))
    print('Errors: '+str(errors))
    print('Post IDs: '+str(posts))
    print('------------------\n')
    return ids

def remove_duplicates(x):
    return list(dict.fromkeys(x))

# main
def main_deprecated():
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)

    tweet_ids = remove_duplicates(extract_ids_from_file())
    create_file()
    err_ids = []

    for tweet_id in tweet_ids:
        print(tweet_id)

    f = open(ERROR_FILE,'w')
    f.write('ids')
    for tweet_id in err_ids:
        f.write('\n'+str(tweet_id))
    f.close()
    print(str(len(err_ids))+' Errors')

def main():
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)

    f = open(ERROR_FILE,'w')
    f.write('ids')

    processed_df = ' , '.join(pd.read_csv(PROCESSED_IDS)['tweet_id'])

    with open(INPUT_NAME) as json_file:
        data = json.load(json_file)
    count_ids = 0
    for item in data:
        for tweet_id in set(item['twitter_ids']):
            if(processed_df.find(tweet_id) == -1 and len(tweet_id) > 5):
                count_ids = count_ids + 1
                print('['+str(count_ids)+'] '+str(tweet_id))

            tweet_id = tweet_id.replace('_','')
            try:
                #tweet = api.get_status(str(tweet_id))
                with open (FILE_NAME, 'a+', newline='') as csvFile:
                    csvWriter = csv.writer(csvFile)
                    tweets_encoded = tweet.text.encode('utf-8')
                    tweets_decoded = tweets_encoded.decode('utf-8')
                    csvWriter.writerow([
                        rc('_'+str(tweet.id)), 
                        rc('_'+str(tweet.user.id)),
                        rc(tweets_decoded), 
                        rc(tweet.created_at), 
                        rc(tweet.geo), 
                        rc(tweet.place.name) if tweet.place else None, 
                        rc(tweet.coordinates), 
                        rc(tweet._json["user"]["location"]), 
                        tweet.favorite_count, 
                        tweet.retweet_count, 
                        tweet.user.followers_count, 
                        rc(tweet.lang)])
            except:
                #print('['+str(tweet_id)+'] - Error')
                f.write('\n'+str(tweet_id))
                pass

main()