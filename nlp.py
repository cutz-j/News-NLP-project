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
        tmp_dict = {}
        tmp_list = []
        tmp_list_body = []
        for k, l in twit.pos(i, norm=True, stem=True):
            if l == 'Noun' or l =='Adjective':
                if len(k) > 1:
                    tmp_list.append(k)
        for k, l in twit.pos(j, norm=True, stem=True):
            if l == 'Noun' or l =='Adjective':
                if len(k) > 1:
                    tmp_list_body.append(k)
        tmp_dict['header'] = tmp_list
        tmp_dict['body'] = tmp_list_body
        res.append(tmp_dict)
    return res

if __name__ == "__main__":
    h_noun = noun(h_art)
    j_noun = noun(j_art)
    h = pd.DataFrame(h_noun)
    h.to_excel("d:/news_project/h_noun.xlsx", header=None, index=None, encoding='utf-8')
    j = pd.DataFrame(j_noun)
    j.to_excel("d:/news_project/j_noun.xlsx", header=None, index=None, encoding='utf-8')