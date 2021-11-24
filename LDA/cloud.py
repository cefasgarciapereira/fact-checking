import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models import CoherenceModel
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer 
import nltk
nltk.download('stopwords')
import pandas as pd
import re
import math
from matplotlib import pyplot as plt
from matplotlib import gridspec
import os
from wordcloud import WordCloud
clear = lambda: os.system('clear')
nltk.download('punkt')

INPUT_FILE='tweet_output_false.csv'
TEXT_COL = 'text_en'
LDA_FILE_OUT = 'lda_output_tweets.txt'
LDA_FIG_OUT = 'lda_output_tweets.png'
COHERENCE_FIG = 'coherence.png'

def clean_tweets(df='', 
                 tweet_col='text_en', 
                ):
    ps = PorterStemmer() 
    df_copy = df.copy()
    
    # drop rows with empty values
    #df_copy.dropna(inplace=True)    
    
    # lower the tweets
    df_copy['preprocessed_' + tweet_col] = df_copy[tweet_col].str.lower()
    
    # filter out stop words and URLs
    en_stop_words = set(stopwords.words('english'))
    extended_stop_words = en_stop_words | \
                        {
                            '&amp;', 'rt',                           
                            'th','co', 're', 've', 'kim', 'daca', 'it', 'one', 'us', 'nan', 'dy'
                        }
    url_re = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'        
    df_copy['preprocessed_' + tweet_col] = df_copy['preprocessed_' + tweet_col].apply(lambda row: ' '.join([str(word) for word in str(row).split() if (not word in extended_stop_words) and (not re.match(url_re, str(word)))]))

    # steem words
    def steemer(words):
        steemed_words = []        
        for w in words: 
            steemed_words.append(ps.stem(str(w)))
        return steemed_words
    
    # tokenize the tweets
    tokenizer = RegexpTokenizer(r'[a-zA-Z]\w+\'?\w*')
    df_copy['tokenized_' + tweet_col] = df_copy['preprocessed_' + tweet_col].apply(lambda row: steemer(tokenizer.tokenize(row)))
    return df_copy


def get_most_freq_words(str, n=None):
    vect = CountVectorizer().fit(str)
    bag_of_words = vect.transform(str)
    sum_words = bag_of_words.sum(axis=0) 
    freq = [(word, sum_words[0, idx]) for word, idx in vect.vocabulary_.items()]
    freq = sorted(freq, key = lambda x: x[1], reverse=True)
    return freq[:n]

df_tweets = pd.read_csv(INPUT_FILE)
df_tweets_clean = clean_tweets(df=df_tweets)
most_freq_words = get_most_freq_words([ word for tweet in df_tweets_clean.tokenized_text_en for word in tweet],len(df_tweets_clean))

#generate wordcloud
wordcloud = WordCloud()
wordcloud.generate_from_frequencies(frequencies=dict(most_freq_words))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('wordcloud.png')