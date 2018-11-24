### W2V 2 models ###
import numpy as np
import pandas as pd
from gensim.models import word2vec as w2v
import multiprocessing
import os
import sklearn.manifold

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
model = None

def word2vector(noun, word_list):
    global model
    num_features = int(len(noun) / 2)
    min_word_count = 3
    num_workers = multiprocessing.cpu_count()
    window_size = 5
    seed = 1
    downsampling = 1e-3
    sample = [noun[i,0].split(",") + noun[i,1].split(",") for i in range(num_features)]
    model = w2v.Word2Vec(sg=1, seed=seed, workers=num_workers, size=num_features, 
                         min_count=min_word_count, window=window_size, sample=downsampling, 
                         iter=30)
    model.build_vocab(sample)
    print(len(model.wv.vocab))
    model.train(sample, total_examples=model.corpus_count, epochs=model.epochs)
    for word in word_list:
        print("%s's positive similarity: " %(word), model.most_similar(positive=[word]))
        print("%s's negative similarity: " %(word), model.most_similar(negative=[word]))
        
word2vector(j_noun, ['원전', '원자력'])
word2vector(h_noun, ['원전', '원자력'])

# matrix #
#tsne = sklearn.manifold.





