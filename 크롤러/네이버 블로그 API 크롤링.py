import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import pandas as pd
from konlpy.tag import Okt
import bs4
from selenium.common.exceptions import TimeoutException


query = input("저장이름 입력")
source = "네이버 블로그"
keyword = input('검색어떤걸로 함')

t = Okt()
now = datetime.now()  # 파일이름 현 시간으로 저장하기
RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/crwa/'  # 결과 저장할 경로/파일명 (본인 경로로 수정)
outputFileName = query + '%s-%s-%s  %s시 %s분.csv' % (
    now.year, now.month, now.day, now.hour, now.minute)

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)


def clean_text(text_in_file):
    text_in_file_1th = re.sub('[a-zA-Z]', '', text_in_file)
    text_in_file_2th = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', text_in_file_1th)

    return text_in_file_2th


def save_csv(RR):
    try:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["Keyword", "Contents", "Words", "Source", "URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')
    except:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["URL"]
        df.to_csv(RESULT_PATH + '블로그 URL 리스트' + outputFileName, mode='w')


def read_url(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    df2 = df['0']
    driver.implicitly_wait(3)
    all = []
    pn = 1
    try:
        for url in df2:
            print(pn)
            pn = pn + 1
            time.sleep(1)
            body_list = [keyword]
            driver.get(url)
            current_url = driver.current_url
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, 'html.parser')
            time.sleep(2)
            try:
                driver.switch_to.frame('mainFrame')
                try:
                    tbody = driver.find_elements_by_id('postViewArea')
                    for txt in tbody:
                        c_txt = txt.text.replace('\n', '')
                        print(txt.text.replace('\n', ''))
                        word = t.nouns(c_txt)
                        word = str(word).strip('[]')
                        print(word)
                        body_list.append(c_txt)
                        body_list.append(word)
                        body_list.append(source)
                        body_list.append(current_url)
                except:
                    pass
                try:
                    tbody = driver.find_elements_by_class_name('se-main-container')
                    for txt in tbody:
                        c_txt = txt.text.replace('\n', '')
                        print(txt.text.replace('\n', ''))
                        word = t.nouns(c_txt)
                        word = str(word).strip('[]')
                        print(word)
                        body_list.append(c_txt)
                        body_list.append(word)
                        body_list.append(source)
                        body_list.append(current_url)
                except:
                    pass
                try:
                    tbody = driver.find_elements_by_class_name('se_component_wrap')
                    ttt = tbody[1]
                    c_txt = ttt.text.replace("\n", "")
                    print(c_txt)
                    word = t.nouns(c_txt)
                    word = str(word).strip('[]')
                    print(word)
                    body_list.append(c_txt)
                    body_list.append(word)
                    body_list.append(source)
                    body_list.append(current_url)
                except:
                    pass
            except:
                pass
            try:
                driver.switch_to.frame('hiddenFrame')
                try:
                    tbody = driver.find_elements_by_id('postViewArea')
                    for txt in tbody:
                        c_txt = txt.text.replace('\n', '')
                        print(txt.text.replace('\n', ''))
                        word = t.nouns(c_txt)
                        word = str(word).strip('[]')
                        print(word)
                        body_list.append(c_txt)
                        body_list.append(word)
                        body_list.append(source)
                        body_list.append(current_url)
                except:
                    pass
                try:
                    tbody = driver.find_elements_by_class_name('se-main-container')
                    for txt in tbody:
                        c_txt = txt.text.replace('\n', '')
                        print(txt.text.replace('\n', ''))
                        word = t.nouns(c_txt)
                        word = str(word).strip('[]')
                        print(word)
                        body_list.append(c_txt)
                        body_list.append(word)
                        body_list.append(source)
                        body_list.append(current_url)
                except:
                    pass
                try:
                    tbody = driver.find_elements_by_class_name('se_component_wrap')
                    ttt = tbody[1]
                    c_txt = ttt.text.replace("\n", "")
                    print(c_txt)
                    word = t.nouns(c_txt)
                    word = str(word).strip('[]')
                    print(word)
                    body_list.append(c_txt)
                    body_list.append(word)
                    body_list.append(source)
                    body_list.append(current_url)
                except:
                    pass
            except:
                pass
            try:
                frame = soup.find_all('frame', {'id':'screenFrame'})
                for i in frame:
                    screen_src = i['src']
                    # print(screen_src)
                    driver.get(screen_src)
                    driver.switch_to.frame('mainFrame')
                    try:
                        tbody = driver.find_elements_by_id('postViewArea')
                        for txt in tbody:
                            c_txt = txt.text.replace('\n', '')
                            print(txt.text.replace('\n', ''))
                            word = t.nouns(c_txt)
                            word = str(word).strip('[]')
                            print(word)
                            body_list.append(c_txt)
                            body_list.append(word)
                            body_list.append(source)
                            body_list.append(current_url)
                    except:
                        pass
                    try:
                        tbody = driver.find_elements_by_class_name('se-main-container')
                        for txt in tbody:
                            c_txt = txt.text.replace('\n', '')
                            print(txt.text.replace('\n', ''))
                            word = t.nouns(c_txt)
                            word = str(word).strip('[]')
                            print(word)
                            body_list.append(c_txt)
                            body_list.append(word)
                            body_list.append(source)
                            body_list.append(current_url)
                    except:
                        pass
                    try:
                        tbody = driver.find_elements_by_class_name('se_component_wrap')
                        ttt = tbody[1]
                        c_txt = ttt.text.replace("\n", "")
                        print(c_txt)
                        word = t.nouns(c_txt)
                        word = str(word).strip('[]')
                        print(word)
                        body_list.append(c_txt)
                        body_list.append(word)
                        body_list.append(source)
                        body_list.append(current_url)
                    except:
                        pass
            except:
                pass
            if(len(body_list) == 5):
                all.append(body_list)


    except TimeoutException as e:
        print('오류 다음으로 넘어갑니다', format(type(e)))

    save_csv(all)


if __name__ == '__main__':
    read_url('세제2019-8-19  14시 37분.csv')