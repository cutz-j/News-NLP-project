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
    res_header, res_body = [], []
    twit = Twitter()
    for i, j in wordList:
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
            tmp_a = ",".join(tmp_list)
            tmp_b = ",".join(tmp_list_body)
        res_header.append(tmp_a)
        res_body.append(tmp_b)
    return res_header, res_body

if __name__ == "__main__":
    h_header, h_body = noun(h_art)
    j_header, j_body = noun(j_art)
    h = pd.concat((pd.DataFrame(h_header), pd.DataFrame(h_body)), axis=1)
    j = pd.concat((pd.DataFrame(j_header), pd.DataFrame(j_body)), axis=1)
    h.to_excel("d:/news_project/h_noun.xlsx", header=None, index=None, encoding='utf-8')
    j.to_excel("d:/news_project/j_noun.xlsx", header=None, index=None, encoding='utf-8')
