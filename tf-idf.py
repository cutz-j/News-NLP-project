### Tf-idf 단어 별 빈도 이해 ###
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os

## load_excel -> 한겨레, 중앙 ##
os.chdir("d:/news_project/")
j_noun = pd.read_excel("j_noun.xlsx", header=None, index=None)
h_noun = pd.read_excel("h_noun.xlsx", header=None, index=None)

# 결측치 처리 #
j_noun = j_noun.dropna()
h_noun = h_noun.dropna()

j_noun = np.array(j_noun)
h_noun = np.array(h_noun)

tfidf = TfidfVectorizer()
tfs = tfidf.fit_transform(j_noun[:,1])
