import pandas as pd
from textblob import TextBlob
from matplotlib import colors
import matplotlib.pyplot as plt
import seaborn as sns

def isNaN(string):
    return string != string


def contains_word(word, string):
    if str(string).find(str(word)) != int('-1'):
        return True
    return False

def sentiment(text):
    if(not isNaN(text)):
        return TextBlob(text).sentiment
    return 0


def facebook():
    facebook = pd.read_csv('./Facebook/facebook.csv')
    facebook = facebook.dropna(subset=['content_en'])
    facebook['subjectivity'] = facebook.apply(lambda x: sentiment(x['content_en']).subjectivity if not isNaN(x['content_en']) else 0, axis=1)
    facebook['polarity'] = facebook.apply(lambda x: sentiment(x['content_en']).polarity if not isNaN(x['content_en']) else 0, axis=1)
    print(facebook.head(10))
    facebook.to_csv('./Sentiment/facebook.csv')

    #Plotting
    fig, (ax1, ax2) = plt.subplots(1,2)
    
    #polarity, ax1
    polarity = facebook['polarity']
    polarity = polarity[polarity != 0]
    sns.distplot(polarity, ax=ax1, axlabel="Polaridade")
    ax1.set_xlim(-1,1)
    ax1.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax1.set_ylabel('Densidade')

    #subjectivity, ax2
    subjectivity = facebook['subjectivity']
    subjectivity = subjectivity[subjectivity != 0]
    sns.distplot(subjectivity, ax=ax2, axlabel="Subjetividade")
    ax2.set_xlim(0,1)
    ax2.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax2.set_ylabel('Densidade')

    plt.tight_layout()
    plt.savefig('./Sentiment/facebook_sentiment.jpg')

    #Generate Hist2d
    fig, ax = plt.subplots(tight_layout=True)
    hist = ax.hist2d(facebook['polarity'], facebook['subjectivity'],  norm=colors.LogNorm())
    ax.set_ylabel('Subjetividade')
    ax.set_xlabel('Polaridade')
    plt.savefig('./Sentiment/facebook_hist2d.jpg')

def facebook_by_country():
    #get list of countries
    countries = pd.read_csv('./Sentiment/countries.csv')
    countries = countries.dropna(subset=['countries'])

    #get tweets with texnt and extract sentiments
    facebook = pd.read_csv('./Facebook/facebook.csv')
    facebook = facebook.dropna(subset=['content_en'])
    facebook['subjectivity'] = facebook.apply(lambda x: sentiment(x['content_en']).subjectivity if not isNaN(x['content_en']) else 0, axis=1)
    facebook['polarity'] = facebook.apply(lambda x: sentiment(x['content_en']).polarity if not isNaN(x['content_en']) else 0, axis=1)

    new_countries = []

    for j, facebook_row in facebook.iterrows():
        for i, country_row in countries.iterrows():
            if(contains_word(country_row['countries'], facebook_row['countries'])):
                country_row['subjectivity'] = facebook_row['subjectivity']
                country_row['polarity'] = facebook_row['polarity']
                new_countries.append(country_row)
    df = pd.DataFrame(new_countries, columns=['countries', 'polarity', 'subjectivity'])
    df.to_csv('./Sentiment/facebook_by_country.csv')

def twitter():
    twitter = pd.read_csv('./Twitter/twitter.csv')
    twitter = twitter.dropna(subset=['text_en'])
    twitter['subjectivity'] = twitter.apply(lambda x: sentiment(x['text_en']).subjectivity if not isNaN(x['text_en']) else 0, axis=1)
    twitter['polarity'] = twitter.apply(lambda x: sentiment(x['text_en']).polarity if not isNaN(x['text_en']) else 0, axis=1)
    print(twitter.head(10))
    twitter.to_csv('./Sentiment/twitter.csv')

    #Plotting
    fig, (ax1, ax2) = plt.subplots(1,2)
    
    #polarity, ax1
    polarity = twitter['polarity']
    polarity = polarity[polarity != 0]
    sns.distplot(polarity, ax=ax1, axlabel="Polaridade")
    ax1.set_xlim(-1,1)
    ax1.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax1.set_ylabel('Densidade')

    #subjectivity, ax2
    subjectivity = twitter['subjectivity']
    subjectivity = subjectivity[subjectivity != 0]
    sns.distplot(subjectivity, ax=ax2, axlabel="Subjetividade")
    ax2.set_xlim(0,1)
    ax2.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax2.set_ylabel('Densidade')

    plt.tight_layout()
    plt.savefig('./Sentiment/twitter_sentiment.jpg')

    #Generate Hist2d
    fig, ax = plt.subplots(tight_layout=True)
    hist = ax.hist2d(twitter['polarity'], twitter['subjectivity'],  norm=colors.LogNorm())
    ax.set_ylabel('Subjetividade')
    ax.set_xlabel('Polaridade')
    plt.savefig('./Sentiment/twitter_hist2d.jpg')

def twitter_by_country():
    #get list of countries
    countries = pd.read_csv('./Sentiment/countries.csv')
    countries = countries.dropna(subset=['countries'])

    #get tweets with texnt and extract sentiments
    twitter = pd.read_csv('./Twitter/twitter.csv')
    twitter = twitter.dropna(subset=['text_en'])
    twitter['subjectivity'] = twitter.apply(lambda x: sentiment(x['text_en']).subjectivity if not isNaN(x['text_en']) else 0, axis=1)
    twitter['polarity'] = twitter.apply(lambda x: sentiment(x['text_en']).polarity if not isNaN(x['text_en']) else 0, axis=1)

    new_countries = []

    for j, twitter_row in twitter.iterrows():
        for i, country_row in countries.iterrows():
            if(contains_word(country_row['countries'], twitter_row['countries'])):
                country_row['subjectivity'] = twitter_row['subjectivity']
                country_row['polarity'] = twitter_row['polarity']
                new_countries.append(country_row)
    df = pd.DataFrame(new_countries, columns=['countries', 'polarity', 'subjectivity'])
    df.to_csv('./Sentiment/twitter_by_country.csv')

facebook_by_country()