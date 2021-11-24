import tweepy
import secrets
import pandas as pd
import random

#set up tweepy
auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth)


df = pd.read_csv('tweet_out_screen_name.csv')
screen_names = list(df['screen_name'])
unique_screen_names = list(set(screen_names))
bot_lvls = []

for name in unique_screen_names:
    bot_lvls.append(random.random())

data = {'screen_names':unique_screen_names, 'bot_levels':bot_lvls}  
df = pd.DataFrame(data)
df.to_csv('./users_bot_lvl.csv')