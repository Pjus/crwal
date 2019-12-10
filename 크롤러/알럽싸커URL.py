from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from datetime import datetime
import pandas as pd
import bs4
import requests
from collections import OrderedDict
from konlpy.tag import Okt

t = Okt
cafe_name = '아이러브싸커'
keyword = input("찾으시려는 키워드를 입력하세요:")
page = input("게시글 페이지 수 입력하세요:")
source = "아이러브싸커"

now = datetime.now()  # 파일이름 현 시간으로 저장하기
RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/crwa/'  # 결과 저장할 경로/파일명 (본인 경로로 수정)
outputFileName = cafe_name +'-'+ keyword + '%s-%s-%s  %s시 %s분.csv' % (
    now.year, now.month, now.day, now.hour, now.minute)

driver = webdriver.Chrome("./chromedriver.exe")

def save_csv(RR):
    try:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["Keyword", "Date", "Contents", "Source", "URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')
    except:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')


def cafe():
    url = "http://cafe.daum.net/WorldcupLove"  # input("접속하기 원하는 카페 url을 입력하세요:")

    # 크롬 드라이버 위치

    # 카페접속
    driver.get(url)
    time.sleep(2)

    # 카페 검색창에 검색어 입력하기
    driver.switch_to.frame('down')
    key = driver.find_element_by_css_selector('input#search_left_query')
    key.send_keys(keyword)
    try:
        driver.find_element_by_css_selector('#cafemenu > div.searchBox.searchBg > a').click()
    except:
        pass
    try:
        driver.find_element_by_css_selector('#cafe-search > form > button').click()
    except:
        pass

    driver.find_element_by_css_selector('#primaryContent > table > tbody > tr.pos_rel > td.cb.pos_rel > div.search_box_wrap.search_box_top_new.bg_sub > div > a.btn_detail').click()
    driver.implicitly_wait(2)
    driver.find_element_by_css_selector('#selectAllMenu').click()
    driver.implicitly_wait(2)
    driver.find_element_by_css_selector('#check_IC6M').click()

    time.sleep(2)
    driver.find_element_by_css_selector('#detail_search_wrap > div > div > a:nth-child(1) > img').click()
    driver.find_element_by_css_selector('#viewListBtn').click()
    driver.implicitly_wait(1)
    driver.find_element_by_css_selector('#viewListLayer > ul > li:nth-child(5) > a').click()

    url_list = []
    k = 1
    pn = 1

    while (pn <= int(page)):
        """
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[1]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[2]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[3]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[4]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[5]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[6]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[7]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[7]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[7]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[7]
        //*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a[7]
        """
        driver.find_element_by_xpath('//*[@id="primaryContent"]/table/tbody/tr[2]/td[2]/div[3]/div/a['+ str(k) +']').click()
        k = k + 1
        pn = pn + 1
        i = 1
        time.sleep(2)
        if (k == 8):
            k = 7
        while (i <= 99):
            # searchCafeList > tbody > tr:nth-child(39) > td.subject.searchpreview_subject > a
            url = driver.find_elements_by_xpath('//*[@id="searchCafeList"]/tbody/tr[' + str(i) + ']/td[2]/a[1]')
            # print(url)
            for li in url:
                url_li = li.get_attribute('href')
                url_list.append(url_li)
                # print(url_li)
            i = i + 2
    for j in url_list:
        print(j)
    save_csv(url_list)



def read_url(filename):
    all = []
    bodd = []
    df = pd.read_csv(filename, encoding='utf-8')
    df2 = df['URL']
    for row in df2:
        result = [keyword]

        # print(row)
        time.sleep(1)
        driver.get(row)
        driver.switch_to.frame('down')
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        try:
            body = driver.find_elements_by_css_selector('#user_contents > table.protectTable > tbody > tr > td')
        except:
            body = driver.find_elements_by_css_selector("#user_contents")

        date = soup.findAll('span', {'class': 'p11 ls0'})
    #
        for d in date:
            dt = d.text
            result.append(dt)
            print("date : {}".format(dt))

        for bodyy in body:
            v = bodyy.text
            cv = v.replace("\n", "")
            bodd.append(cv)

            print("body : {}".format(cv))
            print(type(cv))

            result.append(cv)




        result.append(source)
        result.append(row)
        all.append(result)

    save_csv(all)



if __name__ == '__main__':
    cafe()
    read_url('아이러브싸커-땀 냄새2019-8-18  14시 28분.csv')
