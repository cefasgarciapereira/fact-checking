import pandas as pd

#read csv data
df = pd.read_csv('tweet_out_screen_name.csv')
screen_names = list(df['screen_name'])
unique_screen_names = list(set(screen_names))

accounts = []

with open('users_bot_lvl3.csv', 'w', encoding='UTF8') as f:
    for name in unique_screen_names:
        accounts.append(str("@"+name))

print(accounts)