import tweepy
import csv
import pandas as pd
import math
import secrets
import json
import time
import re

INPUT_NAME = 'poynter_social_false.json'
FILE_NAME = 'tweet_out_screen_name.csv'

def clean_text(text):                                                                                                      
    new_text = text.replace(',',' ')                                                                                        
    new_text = text.replace('\n',' ')                                                                                       
    return new_text 

def create_file():
    with open (FILE_NAME, 'a+', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow([
            'id',
            'title',
            'checked_link',
            'countries',
            'date',
            'justify',
            'label',
            'source',
            "poynter_link",
            "social_medias",

            'tweet_id', 
            'user_id',
            'screen_name',
            'text', 
            'created_at', 
            'geo', 
            'place_name', 
            'coordinates', 
            'user_location', 
            'likes', 
            'retweets', 
            'followers', 
            'lang'])

def extract_ids_from_file():
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

def main_deprecated():
    # main
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)

    tweet_ids = remove_duplicates(extract_ids_from_file())
    create_file()
    err_ids = []

    for tweet_id in tweet_ids:
        try:
            tweet = api.get_status(str(tweet_id))
            with open (FILE_NAME, 'a+', newline='') as csvFile:
                csvWriter = csv.writer(csvFile)
                tweets_encoded = tweet.text.encode('utf-8')
                tweets_decoded = tweets_encoded.decode('utf-8')
                csvWriter.writerow([rc('_'+str(tweet.id)), rc('_'+str(tweet.user.id)),rc(tweets_decoded), rc(tweet.created_at), rc(tweet.geo), rc(tweet.place.name) if tweet.place else None, rc(tweet.coordinates), rc(tweet._json["user"]["location"]), tweet.favorite_count, tweet.retweet_count, tweet.user.followers_count, rc(tweet.lang)])
        except:
            err_ids.append(tweet_id)
            print('['+str(tweet_id)+'] - Error')
            pass

    f = open('errors_all.csv','w')
    f.write('ids')
    for tweet_id in err_ids:
        f.write('\n'+str(tweet_id))
    f.close()
    print(str(len(err_ids))+' Errors')

def main():
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)
    total_tweets = []
    counter = 0
    
    create_file()
    f = open('errors_archive.csv','w')
    f.write('ids')


    with open(INPUT_NAME) as json_file:
        data = json.load(json_file)

    count_ids = 0
    for item in data:
        for tweet_id in item['twitter_ids']:
            total_tweets.append(tweet_id)
    
    for item in data:
        for tweet_id_ in item['twitter_ids']:
            tweet_id = str(tweet_id_).replace('_', '')
            try:
                tweet = api.get_status(str(tweet_id))
                with open (FILE_NAME, 'a+', newline='') as csvFile:
                    csvWriter = csv.writer(csvFile)
                    tweets_encoded = tweet.text.encode('utf-8')
                    
                    tweets_decoded = tweets_encoded.decode('utf-8')
                    csvWriter.writerow([
                        clean_text(str(item['id'])),
                        clean_text(str(item['title'])),
                        clean_text(str(item['checked_link'])),
                        clean_text(str(item['countries'])),
                        clean_text(str(item['date'])),
                        clean_text(str(item['justify'])),
                        clean_text(str(item['label'])),
                        clean_text(str(item['source'])),
                        clean_text(str(item["poynter_link"])),
                        clean_text(str(item["social_medias"])),

                        clean_text('_'+str(tweet.id)), 
                        clean_text('_'+str(tweet.user.id)),
                        clean_text(str(tweet.user.screen_name)),
                        clean_text(str(tweets_decoded)), 
                        tweet.created_at, 
                        clean_text(str(tweet.geo)), 
                        clean_text(str(tweet.place.name)) if tweet.place else None, 
                        clean_text(str(tweet.coordinates)), 
                        clean_text(str(tweet._json["user"]["location"])), 
                        tweet.favorite_count, 
                        tweet.retweet_count, 
                        tweet.user.followers_count, 
                        clean_text(str(tweet.lang))])
            except tweepy.RateLimitError:
                print('Rate Limit Reached!')
                time.sleep(60 * 15)
                continue
            except Exception as e:
                print('['+str(tweet_id)+'] - Error: ', e)
                f.write('['+str(tweet_id)+'] - Error: '+str(e))
                pass
            counter = counter + 1
            print('Progress: ('+str(counter)+"/"+str(len(total_tweets))+")")
main()