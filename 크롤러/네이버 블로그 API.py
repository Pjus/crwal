import requests
from urllib.parse import urlparse
import pandas as pd
from datetime import datetime
import bs4
import re
import pandas as pd
import time
from konlpy.tag import Okt
from selenium.common.exceptions import TimeoutException

keyword = input("검색어 \n")
pn = input("블로그 포스트 수 20단위\n")
t = Okt()
source = "네이버 블로그"

now = datetime.now()  # 파일이름 현 시간으로 저장하기
RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/crwa/'  # 결과 저장할 경로/파일명 (본인 경로로 수정)
outputFileName = keyword + '%s-%s-%s  %s시 %s분.csv' % (
    now.year, now.month, now.day, now.hour, now.minute)

def save_txt(result):
    RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/crwa/'  # 결과 저장할 경로/파일명 (본인 경로로 수정)
    timestr = time.strftime("%Y%m%d-%H%M%S")

    dataWriteHandler = open(RESULT_PATH + timestr + ".txt", "w", encoding='utf-8')
    for items in result:
        print(items, file=dataWriteHandler)
    dataWriteHandler.close()


def save_csv(RR):
    print(RR)
    df = pd.DataFrame(RR)  # df로 변환
    df.columns = ["URL"]
    df.to_csv(RESULT_PATH + outputFileName, mode='w')


def get_blog_url_API():

    client_id = "Yzp2mZspOAofw62rWgeJ"
    client_secret = "5Imu352v7i"

    nblock = int(int(pn) / 20)
    url = []
    url_list = []
    for i in range(0, nblock):
        start = i * 20 + 1 #검색 시작 위치로 1부터 최대 1000까지 가능
        url.append("https://openapi.naver.com/v1/search/blog?query="+keyword+"$&display=20&start="+str(start)+"&sort=sim")
    for ro in url:
        result = requests.get(urlparse(ro).geturl(),
                              headers = {
                                  "X-Naver-Client-Id":client_id,
                                  "X-Naver-Client-Secret":client_secret
                              })
        data = result.json()
        item = data['items']
        for i in item:
            url_list.append(i['link'])

    for i in url_list:
        print(i)

    save_csv(url_list)

if __name__ == '__main__':
    get_blog_url_API()