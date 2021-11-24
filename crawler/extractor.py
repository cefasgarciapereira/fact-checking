import pandas as pd

df = pd.read_csv('./poynter_social_all.csv')
#print(df.head())
df = df[df['social_medias'] == 0]['checked_link']
print(df.head())