import pandas as pd
from textblob import TextBlob

def facebook():
    facebook = pd.read_csv('./Facebook/facebook.csv')
    lda = pd.read_csv('./Facebook/topics.csv')

    new_lda = []

    def contains_word(word, string):
        if str(string).find(str(word)) != int('-1'):
            return True
        return False

    for j, facebook_row in facebook.iterrows():
        print(str(j+1)+'/'+str(len(facebook)))
        for i, lda_row in lda.iterrows():
            if(contains_word(lda_row['Word'], facebook_row['content_en'])):
                interaction_sum = int(facebook_row['all_reactions']) + int(facebook_row['comments']) + int( facebook_row['shares'])
                sentiment = TextBlob(facebook_row['content_en']).sentiment
                new_lda.append([lda_row['Topic'],facebook_row['all_reactions'], facebook_row['comments'], facebook_row['shares'], interaction_sum, sentiment.polarity, sentiment.subjectivity ])
                break
    df = pd.DataFrame(new_lda, columns=['topic','all_reactions', 'comments', 'shares', 'interaction_sum', 'polarity', 'subjectivity'])
    df.to_csv('./Facebook/engajement_facebook_final_sentiment.csv')
    df = df.groupby('topic')
    print(df.describe())


def twitter():
    twitter = pd.read_csv('./Twitter/twitter.csv')
    lda = pd.read_csv('./Twitter/topics.csv')

    new_lda = []

    def contains_word(word, string):
        if str(string).find(str(word)) != int('-1'):
            return True
        return False

    for j, twitter_row in twitter.iterrows():
        print(str(j+1)+'/'+str(len(twitter)))
        for i, lda_row in lda.iterrows():
            if(contains_word(lda_row['Word'], twitter_row['text_en'])):
                try:
                    interaction_sum = int(twitter_row['likes']) + int(twitter_row['retweets']) + int( twitter_row['followers'])
                except Exception:
                    pass
                try:
                    sentiment = TextBlob(twitter_row['text_en']).sentiment
                except Exception:
                    pass

                new_lda.append([lda_row['Topic'],twitter_row['likes'], twitter_row['retweets'], twitter_row['followers'], interaction_sum, sentiment.polarity, sentiment.subjectivity])
                break
    df = pd.DataFrame(new_lda, columns=['topic','likes', 'retweets', 'followers', 'interaction_sum', 'polarity', 'subjectivity'])
    df.to_csv('./Twitter/engajement_twitter_final_sentiment.csv')
    df = df.groupby('topic')
    print(df.describe())

def poynter():
    poynter = pd.read_csv('./Poynter/poynter_false.csv')
    lda = pd.read_csv('./Poynter/topics.csv')

    new_lda = []

    def contains_word(word, string):
        if str(string).find(str(word)) != int('-1'):
            return True
        return False

    for j, poynter_row in poynter.iterrows():
        print(str(j+1)+'/'+str(len(poynter)))
        for i, lda_row in lda.iterrows():
            if(contains_word(lda_row['Word'], poynter_row['justify'])):
                new_lda.append(lda_row['Topic'])

    df = pd.DataFrame(new_lda, columns=['topic'])
    df.to_csv('./Poynter/engajement_poynter_final.csv')

facebook()