import pandas as pd
import pegabot
import csv

#read csv data
df = pd.read_csv('tweet_out_screen_name.csv')
screen_names = list(df['screen_name'])
unique_screen_names = list(set(screen_names))
bot_lvls = []
infos = []
idx = 0
datas = []
header = ['screen_names', 'bot_levels', 'infos']

with open('users_bot_lvl3.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for name in unique_screen_names:
        try:
            idx = idx + 1
            print(name+': '+str(idx)+'/'+str(len(unique_screen_names)))
            res = pegabot.get_bot_probability(name)
            bot_lvl = str(res['all'])
            info = str(res['info'])
            data = [name,bot_lvl,info]
            writer.writerow(data)
            print('ok\n')
        except:
            print('falhou: '+name)
            continue

# close the file
f.close()