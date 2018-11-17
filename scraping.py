### News scraping을 위한 함수 ###
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib import parse
from collections import Counter
import time
from selenium import webdriver

article = [] # parse 결과 담는 list
word_list = ['원전']

for word in word_list:
    url = "https://search.joins.com/JoongangNews?page=1&Keyword="
    url += parse.quote(word)
    url += "&SortType=New&ScopeType=Title&SearchCategoryType=JoongangNews"
    # selenium drvier (chromedriver download)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    results = soup.select("div.text")
    
    for res in results:
        url_article = res.attrs["href"]
        