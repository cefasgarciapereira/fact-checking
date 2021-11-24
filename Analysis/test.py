import pandas as pd
from textblob import TextBlob

text = "Chinese are not people"

print(TextBlob(text).sentiment)