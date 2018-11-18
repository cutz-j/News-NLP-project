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
        for i in range(2, total_page_num): # 총 출력 페이지만큼 페이지 이동
            results = soup.select("div.text")
            for res in results: # 해당 페이지의 기사 10건 접속
                if word not in res.find("a").text: # 제목에 word가 없다면, continue
                    continue
                tmp_list = []
                url_article = res.find("a").attrs["href"] # article href 주소 따오기
                tmp_list.append(res.find("a").text) # 제목 리스트 추가
                html_art = requests.get(url_article) # article 본문 접속
                soup_art = BeautifulSoup(html_art.text, 'html.parser')
                results_art = soup_art.select("div#article_body")
                article = results_art[0].text.strip()
                if "관련기사" in article:
                    reg = re.compile("  관련기사[\w\W]{,80}  \xa0")
                    article = re.sub(reg, "", article)
                article = article.replace("\xa0", "").replace("  ", "")
                article = article[:-article[::-1].index(".다")]
                reg = re.compile("\[[가-힣a-zA-Z0-9=-_/.,:;]*\]")
                article = re.sub(reg, "", article)
                time.sleep(0.2)
                tmp_list.append(article)
                articleList.append(tmp_list)
            print("%i page completed / total page %i" %(i, total_page_num))
            url = url.replace("page=%i" %(i-1), "page=%i" %(i))
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
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
        for i in range(1, total_page_num): # 총 출력 페이지만큼 페이지 이동
            results = soup.select("dt > a")
            for res in results: # 해당 페이지의 기사 10건 접속
                if word not in res.text: # 제목에 word가 없다면, continue
                    continue
                tmp_list = []
                tmp_list.append(res.text)
                url_article = res.attrs["href"] # article href 주소 따오기
                html_art = requests.get(url_article) # article 본문 접속
                soup_art = BeautifulSoup(html_art.text, 'html.parser')
                results_art = soup_art.select("div.text")
                results_art = results_art[0].text.strip()
                if "※ 그래픽을 누르면 확대됩니다." in results_art:
                    results_art = results_art.replace("※ 그래픽을 누르면 확대됩니다.", "")
                reg_grp = re.compile("그래픽_[가-힣]{3}")
                if re.findall(reg_grp, results_art) != []:
                    results_art = re.sub(reg_grp, "", results_art)
                results_art = results_art[:-results_art[::-1].index(".다")]
                if "@hani.co.kr" in results_art:
                    reg = re.compile("[\w\W]{3,7}[\w\W]{3,5}[a-zA-Z]+@hani.co.kr")
                    results_art = re.sub(reg, "", results_art)
                if "  " in results_art:
                    results_art = results_art[results_art.index("  "):]
                try: results_art = results_art.replace("  ", "")
                except: pass
                tmp_list.append(results_art)
                article_list.append(tmp_list)
                time.sleep(0.2)
            print("%i page completed / total page %i" %(i, total_page_num))
            url = url.replace("pageseq=%i" %(i-1), "pageseq=%i" %(i))
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
    return article_list

if __name__ == "__main__":
    ## parameter ##
    word_list = ['원전', '신고리']
    res_list_1 = joongang_scrape(word_list)
    res_list_2 = hani_scrape(word_list)