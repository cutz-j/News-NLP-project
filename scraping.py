### News scraping을 위한 함수 ###
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib import parse
from collections import Counter
import time
import re

## parameter ##
word_list = ['원전']

def joongang_scrape(word_list):
    ## 원하는 word List의 제목을 가진 기사를 최근 3년 기사를 scrape하는 함수 ##
    articleList = [] # parse 결과 담는 list
    for word in word_list: # 관련 단어 모두 검색
        url = "https://search.joins.com/TotalNews?page=1&Keyword="
        url += parse.quote(word)
        url += "&PeriodType=DirectInput&StartSearchDate=01%2F01%2F2015%2000%3A00%3A00&EndSearchDate=11%2F18%2F2018%2000%3A00%3A00&SortType=New&ScopeType=Title&SourceGroupType=Joongang&SearchCategoryType=TotalNews"
        # selenium drvier (chromedriver download)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        # 총 출력 페이지 parsing #
        total_page_num = soup.select("span.total_number")[0].text
        reg = re.compile("-[0-9]+")
        total_page_num = int(re.findall(reg, total_page_num)[0][1:])
        for i in range(1, total_page_num): # 총 출력 페이지만큼 페이지 이동
            url.replace("page=1", "page=%i" %(i))
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            results = soup.select("div.text")
            for res in results: # 해당 페이지의 기사 10건 접속
                tmp_list = []
                url_article = res.find("a").attrs["href"] # article href 주소 따오기
                tmp_list.append(res.find("a").text) # 제목 리스트 추가
                html_art = requests.get(url_article) # article 본문 접속
                soup_art = BeautifulSoup(html_art.text, 'html.parser')
                results_art = soup_art.select("div#article_body")
                article = results_art[0].text.strip()[:-33]
                reg = re.compile("  관련기사[\w\W]{,80}  \xa0")
                article = re.sub(reg, "", article).replace("\xa0", "").replace("  ", "")
                time.sleep(1)
                tmp_list.append(article)
                articleList.append(tmp_list)
            print("=== %i page completed / total page %i" %(i, total_page_num))
    return articleList

res = pd.DataFrame(articleList)         
res.to_csv("d:/project_data/article_1.csv")       
            
            
            
            
            
            
            
            
            
            
            
            