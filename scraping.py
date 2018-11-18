### News scraping을 위한 함수 ###
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib import parse
from collections import Counter
import time
import re

def joongang_scrape(word_list):
    ## 원하는 word List의 제목을 가진 기사를 모두 scrape하는 함수 ##
    articleList = [] # parse 결과 담는 list
    for word in word_list: # 관련 단어 모두 검색
        url = "https://search.joins.com/TotalNews?page=1&Keyword="
        url += parse.quote(word)
        url += "&SortType=New&ScopeType=Title&SourceGroupType=Joongang&SearchCategoryType=TotalNews"
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
                time.sleep(0.5)
                tmp_list.append(article)
                articleList.append(tmp_list)
            print("=== %i page completed / total page %i" %(i, total_page_num))
    return articleList
            
## 한겨레 최근 3년 기사를 scrape하는 함수 ##
def hani_scrape(word_list):
    article_list = []
    for word in word_list: # 관련 단어 모두 검색
        url = "http://search.hani.co.kr/Search?command=query&keyword="
        url += parse.quote(word)
        url += "&media=news&sort=d&period=all&datefrom=2015.01.01&dateto=2018.11.18&pageseq=0"
        # selenium drvier (chromedriver download)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        # 총 출력 페이지 parsing #
        total_page_num = soup.select("span.total")[0].text
        total_page_num = int(int(total_page_num[:-1]) / 10)
        for i in range(0, total_page_num): # 총 출력 페이지만큼 페이지 이동
            url.replace("pageseq=0", "pageseq=%i" %(0))
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            results = soup.select("dt > a")
            for res in results: # 해당 페이지의 기사 10건 접속
                tmp_list = []
                if word not in res.text: # 제목에 word가 없다면, continue
                    continue
                tmp_list.append(res.text)
                url_article = res.attrs["href"] # article href 주소 따오기
                html_art = requests.get(url_article) # article 본문 접속
                soup_art = BeautifulSoup(html_art.text, 'html.parser')
                results_art = soup_art.select("div.text")
                results_art = results_art[0].text.strip()
                if "@hani.co.kr" in results_art:
                    reg = re.compile("[\w\W]{3,7}[\w\W]{3,5}[a-zA-Z]+@hani.co.kr")
                    results_art = re.sub(reg, "", results_art)
                    res = results_art.replace("\n", "").replace("\r", "").replace("  ", "")
                tmp_list.append(res)
                article_list.append(tmp_list)
                time.sleep(0.5)
            print("=== %i page completed / total page %i" %(i, total_page_num))
    return article_list

if __name__ == "__main__":
    ## parameter ##
    word_list = ['원전', '신고리']
    res_list_1 = joongang_scrape(word_list)
    res_list_2 = hani_scrape(word_list)