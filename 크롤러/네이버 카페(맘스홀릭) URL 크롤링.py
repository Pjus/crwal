import nltk
from konlpy.tag import Kkma
from selenium import webdriver
import time
import re
from datetime import datetime
import pandas as pd
import bs4
from selenium.common.exceptions import TimeoutException
from konlpy.tag import Okt

# 크롬 드라이버 위치


cafe_name = input("카페이름을입력하세요:")
keyword = input("키워드를 입력하세요:")

t = Okt()
source = "네이버 카페"

now = datetime.now()  # 파일이름 현 시간으로 저장하기
RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/crwa/'  # 결과 저장할 경로/파일명 (본인 경로로 수정)
outputFileName = cafe_name +'-'+ keyword + '%s-%s-%s  %s시 %s분.csv' % (
    now.year, now.month, now.day, now.hour, now.minute)


driver = webdriver.Chrome("./chromedriver.exe")
#아이디 패스워드 입력
id = "manchu0220"
pw = "zzalswlzz"

# 네이버 로그인
driver.get('https://nid.naver.com/nidlogin.login')
driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")
driver.find_element_by_css_selector("#frmNIDLogin > fieldset > input").click()
time.sleep(4)


def save_csv(RR):
    try:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["Keyword", "Date", "Title", "Contents", "Words", "Comments", "Source", "URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')
    except:
        df = pd.DataFrame(RR)  # df로 변환
        df.columns = ["URL"]
        df.to_csv(RESULT_PATH + outputFileName, mode='w')


def cafe(filename):

    df = pd.read_csv(filename, encoding='utf-8')
    df2 = df['URL']
    all = []
    try:
        pn = 1
        try:
            for row in df2:
                print(pn)
                pn = pn + 1
                result = [keyword]

                # print(row)
                time.sleep(1)
                driver.get(row)
                try:
                    driver.switch_to.frame('cafe_main')
                    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                    title = soup.findAll('span', {'class': 'b m-tcol-c'})
                    body = soup.findAll('div', {'id': 'tbody'})
                    date = soup.findAll('td', {'class': 'm-tcol-c date'})

                    for d in date:
                        dt = d.text
                        result.append(dt)
                        print("data : {}".format(dt))

                    for m in title:
                        print(m)
                        ti = m.text
                        result.append(ti)
                        print("제목 : {}".format(ti))


                    for i in body:
                        tbody = i.text
                        c_text = tbody.replace('\n', '')
                        result.append(c_text)
                        print("본문 : {}".format(c_text))
                        word = t.nouns(c_text)
                        word = str(word).strip('[]')
                        result.append(word)
                        print("형태소 분석 : {}".format(word))

                    comment = soup.find_all('span', {'class': 'comm_body'})
                    for n in range(0, len(comment)):
                        comment[n] = comment[n].get_text()
                    comment = str(comment).strip('[]')
                    result.append(comment)
                    print("댓글 : {}".format(comment))
                    result.append(source)
                    print("출처 : {}".format(source))
                    result.append(row)
                    if (len(result) == 8):
                        all.append(result)
                except:
                    pass
        except:
            pass
        for gg in result:
            print(gg)
    except TimeoutException as e:
        print('오류 다음으로 넘어갑니다', format(type(e)))
    # save_txt()
    save_csv(all)


if __name__ == '__main__':
    cafe('맘스홀릭-빨래2019-8-19  14시 39분.csv')

