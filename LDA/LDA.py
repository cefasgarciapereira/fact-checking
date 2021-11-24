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
import pandas as pd
import re
import math
from matplotlib import pyplot as plt
from matplotlib import gridspec
from wordcloud import WordCloud
import pickle
nltk.download('stopwords')
nltk.download('punkt')


class LDA:

    def __init__(self, df='', text_column=''):
        self.text_column = text_column
        self.df = df

    def clean_text(self):
        ps = PorterStemmer()
        df_copy = self.df.copy()

        # drop rows with empty values
        #df_copy.dropna(inplace=True)
        df_copy = df_copy[df_copy[self.text_column].notna()]

        # lower the text
        df_copy['preprocessed_' +
                self.text_column] = df_copy[self.text_column].str.lower()

        # filter out stop words and URLs
        en_stop_words = stopwords.words('english')
        
        extended_stop_words = [ 
            'nan', 'dy', '#nocomascuento', 'iâ', 'donâ', 'reâ', 'beeâ', 'abba', 'lola', 
            'kyari', 'realli', 'yesâ', 'improvisingâ', 'ppe', 'wereâ', 'zshamsuna', 'staâ',
            'pertineâ', 'bâ', 'noâ', 'rightâ', 'fwiw', 'wâ', 'maneraâ', 'oâ', 'co', 'kuhakikishaâ', 'backâ'
            'zagreb', 'backâ', 'get', 'explanation'
            ]

        extended_stop_words = extended_stop_words + en_stop_words
        url_re = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
        df_copy['preprocessed_' + self.text_column] = df_copy['preprocessed_' + self.text_column].apply(lambda row: ' '.join(
            [str(word) for word in str(row).split() if (not word in extended_stop_words) and (not re.match(url_re, str(word)))]))

        # steem words
        def steemer(words):
            steemed_words = []
            for w in words:
                steemed_words.append(ps.stem(str(w)))
            return steemed_words

        # tokenize the tweets
        tokenizer = RegexpTokenizer(r'[a-zA-Z]\w+\'?\w*')
        df_copy['tokenized_' + self.text_column] = df_copy['preprocessed_' +
                                                           self.text_column].apply(lambda row: steemer(tokenizer.tokenize(row)))
        return df_copy

    def get_most_freq_words(self, str, n):
        vect = CountVectorizer().fit(str)
        bag_of_words = vect.transform(str)
        sum_words = bag_of_words.sum(axis=0)
        freq = [(word, sum_words[0, idx])
                for word, idx in vect.vocabulary_.items()]
        freq = sorted(freq, key=lambda x: x[1], reverse=True)
        return freq[:n]
    
    def get_bigrams(self, words):
        bigrams_list = list(nltk.bigrams(words))
        dictionary2 = [' '.join(tup) for tup in bigrams_list]

        #Using count vectoriser to view the frequency of bigrams
        vectorizer = CountVectorizer(ngram_range=(2, 2))
        bag_of_words = vectorizer.fit_transform(dictionary2)
        vectorizer.vocabulary_
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        print (words_freq[:5])

        #Generating wordcloud and saving as png image
        words_dict = dict(words_freq)
        WC_height = 1000
        WC_width = 1500
        WC_max_words = 200
        wordcloud = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width, background_color='white')
        wordcloud.generate_from_frequencies(words_dict)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        wordcloud.to_file('./assets/output/wordcloud_bigram.jpg')
        print('Wordcloud bigram generated')


    def get_wordcloud(self, most_freq_words):
        # generate wordcloud
        WC_height = 1000
        WC_width = 1500
        WC_max_words = 200
        wordcloud = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width, background_color='white')
        wordcloud.generate_from_frequencies(frequencies=dict(most_freq_words))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        wordcloud.to_file('./assets/output/wordcloud.jpg')
        print('Wordcloud generated')

    def compute_coherence(self, corpus, text_dictionary, n_tests=35):
        # compute coherence and returns the number of topics with highest coherence
        print('Computing coherence')
        coherences = []
        for nb_topics in range(1,n_tests):
            print(str(nb_topics)+'/'+str(n_tests))
            lda = LdaModel(corpus, num_topics = nb_topics, id2word = text_dictionary, passes=10)
            cohm = CoherenceModel(model=lda, corpus=corpus, dictionary=text_dictionary, coherence='u_mass')
            coh = cohm.get_coherence()
            coherences.append(coh)

        #visualize coherence
        plt.figure(figsize=(10,5))
        plt.plot(range(1, n_tests),coherences)
        plt.xlabel("Número de Tópicos")
        plt.ylabel("Taxa de Coerência")
        plt.show()
        plt.savefig('./assets/output/coherence.png')

        max_coherence_k = coherences.index(max(coherences)) + 1

        print("Max coherence: K: "+str(max_coherence_k)+" Coh: "+str(max(coherences)))

        return max_coherence_k
    
    def lda_runner(self, corpus, text_dictionary, k, n_words):
        # runs LDA itself
        print('Running LDA: K('+str(k)+') W('+str(n_words)+')')
        text_lda = LdaModel(corpus, num_topics = k, id2word = text_dictionary, passes=10)

        def plot_top_words(lda=text_lda, nb_topics=k, nb_words=n_words):
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
            plt.savefig('./assets/output/lda_output.png')

        #write LDA output in file
        top_words_per_topic = []
        for t in range(text_lda.num_topics):
            top_words_per_topic.extend([(t, ) + x for x in text_lda.show_topic(t, topn = 20)])
        pd.DataFrame(top_words_per_topic, columns=['Topic', 'Word', 'P']).to_csv("./assets/output/top_words.csv")
        #plot LDA
        plot_top_words()

    def start(self, n_tests = 2, k = 2, n_words = 20, use_max_coherence = True):
        df_clean = self.clean_text()
        print(df_clean.head())
        print(df_clean.shape)
        print(len(df_clean))
        most_freq_words = self.get_most_freq_words([word for text in df_clean.tokenized_justify for word in text], len(df_clean))
        print(most_freq_words[:10])
        self.get_wordcloud(most_freq_words)
        self.get_bigrams([word for text in df_clean.tokenized_justify for word in text])

        # build a dictionary where for each text, each word has its own id.
        text_dictionary = Dictionary(df_clean.tokenized_justify)
        
        # build the corpus i.e. vectors with the number of occurence of each word per tweet
        corpus = [text_dictionary.doc2bow(text) for text in df_clean.tokenized_justify]
        
        if use_max_coherence == True:
            max_coherence_k = self.compute_coherence(corpus = corpus, text_dictionary = text_dictionary, n_tests = n_tests)
        else:
            max_coherence_k = k
        
        self.lda_runner(corpus = corpus, text_dictionary = text_dictionary, k = max_coherence_k, n_words = n_words)