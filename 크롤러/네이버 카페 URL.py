import nltk
from konlpy.tag import Okt
from konlpy.tag import Kkma
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from datetime import datetime
import pandas as pd
import bs4
import requests
from collections import OrderedDict


cafe_name = input("카페이름을입력하세요:")
keyword = input("찾으시려는 키워드를 입력하세요:")
page = input("게시글 페이지 수 입력하세요:")
start_date = input('검색시작날짜20000101 형태로 입력')
end_date = input('종료날짜')

source = "네이버 카페"

now = datetime.now()  # 파일이름 현 시간으로 저장하기
RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/crwa/'  # 결과 저장할 경로/파일명 (본인 경로로 수정)
outputFileName = cafe_name +'-'+ keyword + '%s-%s-%s  %s시 %s분.csv' % (
    now.year, now.month, now.day, now.hour, now.minute)


def save_csv(RR):
    try:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["Keyword", "Date", "Title", "Contents", "Words", "Comments", "Source"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')
    except:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')


def cafe():
    url = "https://cafe.naver.com/imsanbu"  # input("접속하기 원하는 카페 url을 입력하세요:")
    # 본인 계정 비번 입력
    id = 'manchu0220'
    pw = 'zzalswlzz'

    # 크롬 드라이버 위치
    driver = webdriver.Chrome("./chromedriver.exe")

    # 네이버 로그인
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")
    driver.find_element_by_css_selector("#frmNIDLogin > fieldset > input").click()
    time.sleep(4)

    # 카페접속
    driver.get(url)
    time.sleep(2)

    # 카페 검색창에 검색어 입력하기
    key = driver.find_element_by_css_selector('input#topLayerQueryInput')
    key.send_keys(keyword)
    try:
        driver.find_element_by_css_selector('#info-search > form > button').click()
    except:
        pass
    try:
        driver.find_element_by_css_selector('#cafe-search > form > button').click()
    except:
        pass

    driver.switch_to.frame('cafe_main')

    driver.find_element_by_css_selector('#currentSearchDateTop').click()
    skey = driver.find_element_by_css_selector('input#input_1_top')
    ekey = driver.find_element_by_css_selector('input#input_2_top')
    skey.clear()
    ekey.clear()
    skey.send_keys(start_date)
    ekey.send_keys(end_date)
    time.sleep(2)
    driver.find_element_by_css_selector('#btn_set_top').click()

    driver.find_element_by_css_selector('#main-area > div.search_result > div:nth-child(1) > form > div.input_search_area > button').click()
    url_list = []
    current_page = 1
    y = 1
    x = 0
    while (current_page <= int(page)):#main-area > div.prev-next > a.on#main-area > div.prev-next > a:nth-child(4)
        for k in range(3, 13):
            mid = k + x
            next_page = driver.find_elements_by_css_selector('#main-area > div.prev-next > a:nth-child(' + str(mid) + ')')
            for nn in next_page:
                nn.click()
            current_page = current_page + 1
            # print(current_page)
            i = 1
            time.sleep(2)
            while (i <= 15):
                # main-area > div.article-board.result-board.m-tcol-c > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a.article
                url = driver.find_elements_by_css_selector(
                    '#main-area > div.article-board.result-board.m-tcol-c > table > '
                    'tbody > tr:nth-child(' + str(i) + ') > td.td_article > div.board-list > div > a.article')
                # print(url)
                for li in url:
                    url_li = li.get_attribute('href')
                    url_list.append(url_li)
                i = i + 1
                # print(i)
        if(y == 1):
            x = 1

    for j in url_list:
        print(j)
    save_csv(url_list)


if __name__ == '__main__':
    cafe()

