### Tf-idf 단어 별 빈도 이해 ###
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os

## load_excel -> 한겨레, 중앙 ##
os.chdir("d:/news_project/")
j_noun = pd.read_excel("j_noun.xlsx", header=None, index=None)
h_noun = pd.read_excel("h_noun.xlsx", header=None, index=None)
j_noun.columns = ['body', 'header']
h_noun.columns = ['body', 'header']

j_noun = j_noun.reindex(columns=['header', 'body'])
h_noun = h_noun.reindex(columns=['header', 'body'])


tfidf = TfidfVectorizer()
tfs = tfidf.fit_transform(h_noun.iloc[0,0][1:-1])
