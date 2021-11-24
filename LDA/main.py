from LDA import LDA
import pandas as pd

INPUT_FILE='./assets/input/poynter_false.csv'

df = pd.read_csv(INPUT_FILE)
lda = LDA(df=df, text_column="justify")
lda.start(n_tests = 40, k=6, n_words = 30, use_max_coherence = False)