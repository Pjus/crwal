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
keyword = input("키워드를 입력하세요:")
source = "아이러브싸커"

now = datetime.now()  # 파일이름 현 시간으로 저장하기
RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/crwa/'  # 결과 저장할 경로/파일명 (본인 경로로 수정)
outputFileName = cafe_name +'-'+ keyword + '%s-%s-%s  %s시 %s분.csv' % (
    now.year, now.month, now.day, now.hour, now.minute)

driver = webdriver.Chrome("./chromedriver.exe")

def save_csv(RR):
    try:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["Keyword", "Date", "Title", "Contents", "Source", "URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')
    except:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')


def read_url(filename):
    all = []
    df = pd.read_csv(filename, encoding='utf-8')
    df2 = df['URL']
    for row in df2:
        result = [keyword]
        # print(row)
        time.sleep(1)
        driver.get(row)
        driver.switch_to.frame('down')
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        title = driver.find_element_by_xpath('//*[@id="bbsForm"]/div[3]/div/span[2]')
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
        result.append(title.text)
        print("제목 : {}".format(title.text))
        for bodyy in body:
            v = bodyy.text
            cv = v.replace("\n", "")
            result.append(cv)
            print("body : {}".format(cv))

        result.append(source)
        result.append(row)
        if (len(result) == 6):
            all.append(result)
    save_csv(all)


if __name__ == '__main__':
    read_url('아이러브싸커-땀 냄새2019-8-18  14시 28분.csv')
