### W2V 2 models ###
import numpy as np
import pandas as pd
from gensim.models import word2vec as w2v
import multiprocessing
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

## parameter ##
num_features = 300
min_word_count = 3
num_workers = multiprocessing.cpu_count()
window_size = 5
seed = 7
downsampling = 1e-3

sample = h_noun[0,1].split(",")

model = w2v.Word2Vec(sg=1, seed=seed, workers=num_workers, size=num_features, min_count=min_word_count,
               window=window_size, sample=downsampling, iter=1000)

model.build_vocab(h_noun[:,1])
model.train(h_noun[:,1], total_examples=model.corpus_count)