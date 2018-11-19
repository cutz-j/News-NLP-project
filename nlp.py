### 형태소 분석 & 전처리 ###
import numpy as np
import pandas as pd
from konlpy.tag import Twitter
from collections import Counter

## data load ##
h_art = pd.read_excel("d:/news_project/res1_h.xlsx", header=None, index=None, encoding='utf-8').dropna()
j_art = pd.read_excel("d:/news_project/res1_test.xlsx", header=None, index=None, encoding='utf-8').dropna()

# 연산 속도를 위해 numpy로 변환 #
h_art = np.array(h_art)
j_art = np.array(j_art)

## 형태소 분석 & 명사 추출 ##
def noun(wordList):
    res = []
    twit = Twitter()
    for i, j in wordList:
        for k, l in twit.pos(i, norm=True, stem=True):
            tmp_list = []
            if l == 'Noun' and len(k) > 1:
                tmp_list.append(k)
        for k, l in twit.pos(j, norm=True, stem=True):
            if l == 'Noun' and len(k) > 1:
                tmp_list.append(k)
        res.append(tmp_list)
    return res

## 빈도 분석 ##

if __name__ == "__main__":
    h_noun = noun(h_art)
    j_noun = noun(j_art)