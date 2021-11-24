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
nltk.download('punkt')

INPUT_FILE='tweet_output_false.csv'
TEXT_COL = 'text_en'

def clean_tweets(df='', 
                 tweet_col=TEXT_COL, 
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
                            'th','co', 're', 've', 'kim', 'daca', 'it', 'one', 'us', 'nan', 'dy', 'nocomascuento'
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
print(df_tweets_clean.head())
print(len(df_tweets_clean))

most_freq_words = get_most_freq_words([ word for tweet in df_tweets_clean.tokenized_text_en for word in tweet],10)
print(most_freq_words)

# build a dictionary where for each tweet, each word has its own id.
# We have 6882 tweets and 10893 words in the dictionary.
tweets_dictionary = Dictionary(df_tweets_clean.tokenized_text_en)

# build the corpus i.e. vectors with the number of occurence of each word per tweet
tweets_corpus = [tweets_dictionary.doc2bow(tweet) for tweet in df_tweets_clean.tokenized_text_en]

# compute coherence
tweets_coherence = []
n_tests = 3
for nb_topics in range(1,n_tests):
    lda = LdaModel(tweets_corpus, num_topics = nb_topics, id2word = tweets_dictionary, passes=10)
    cohm = CoherenceModel(model=lda, corpus=tweets_corpus, dictionary=tweets_dictionary, coherence='u_mass')
    coh = cohm.get_coherence()
    tweets_coherence.append(coh)
    print(str(nb_topics)+'/'+str(n_tests))

#visualize coherence
plt.figure(figsize=(10,5))
plt.plot(range(1, n_tests),tweets_coherence)
plt.xlabel("Number of Topics")
plt.ylabel("Coherence Score")
plt.show()
plt.savefig('coherence.png')

#get bigger coherence index
max_coherence = tweets_coherence[0]
max_coherence_k = 0
i = 0
while i < len(tweets_coherence):
    if tweets_coherence[i] > max_coherence:
        max_coherence = tweets_coherence[i]
        max_coherence_k = i
    i = i + 1
print("Max coherence: K: "+str(max_coherence_k)+" Coh: "+str(max_coherence))

# runs LDA
print('Running LDA')
k = max_coherence_k + 1 # +1 because the first index is 0 and the number of topics can't be 0
k = 14
tweets_lda = LdaModel(tweets_corpus, num_topics = k, id2word = tweets_dictionary, passes=10)

def plot_top_words(lda=tweets_lda, nb_topics=k, nb_words=20):
    top_words = [[word for word,_ in lda.show_topic(topic_id, topn=50)] for topic_id in range(lda.num_topics)]
    top_betas = [[beta for _,beta in lda.show_topic(topic_id, topn=50)] for topic_id in range(lda.num_topics)]

    gs  = gridspec.GridSpec(round(math.sqrt(k))+1, round(math.sqrt(k))+1)
    gs.update(wspace=0.5, hspace=0.5)
    plt.figure(figsize=(20,15))
    for i in range(nb_topics):
        ax = plt.subplot(gs[i])
        plt.barh(range(nb_words), top_betas[i][:nb_words], align='center',color='blue', ecolor='black')
        ax.invert_yaxis()
        ax.set_yticks(range(nb_words))
        ax.set_yticklabels(top_words[i][:nb_words])
        plt.title("Topic "+str(i))     
    plt.show() 
    plt.savefig('lda_output.png')
  
plot_top_words()