from datetime import datetime
import bs4
import requests
import pandas as pd
import glob


#입력정보 받기

def inputinfo():
    query = input("검색어 입력하시오 \n")
    cat = input("카테고리 입력하시오 뉴스:1 블로그:2\n")
    maxpage = input("최대 검색 페이지수 입력하시오 \n")
    sort = input("정렬순서 정확도1 최신순2 \n")

    category(query, cat, maxpage, sort)

#카테고리 결정하고 신문사 url 요청변수 넣어서 가져오기

def category(query, cat, maxpage, sort):
    page = maxpage
    if (cat == "1"):
        print("===========================")
        press = input("신문사를 선택하시오 중앙일보1 한국경제2 한겨례3 \n")
        if (press == "1"):
            if (sort == "1"):
                sort = "Accuracy"
            else:
                sort = "New"
            j_url(query, sort, page)
        if (press == "2"):
            if (sort =="1"):
                sort = "RANK"
            else:
                sort = "DATE"
            k_url(query, sort, page)
        if (press == "3"):
            if (sort =="1"):
                sort = "s"
            else:
                sort = "d"
            h_url(query, sort, page)
    if(cat == "2"):
        blog_url(query, sort, page)

def j_url(url_info, sort, maxpage):
    pn = 1
    page=1
    url_list = []

    while(pn<=int(maxpage)):
        url = "https://search.joins.com/JoongangNews?Keyword=" + url_info + "&SortType=" + sort + "&SearchCategoryType=JoongangNews&PeriodType=All&ScopeType=All&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&TotalCount=0&StartCount=0&IsChosung=False&IssueCategoryType=All&IsDuplicate=True&Page=" + str(pn) + "&PageSize=10&IsNeedTotalCount=True"
        # print("{} 페이지".format(pn))
        pn = pn + 1
        response = requests.get(url)
        html = response.text
        objBS = bs4.BeautifulSoup(html, "html.parser")

        news_infos = objBS.findAll("h2", {"class":"headline mg"})

        #print(news_infos)
        for i in news_infos:
             a_h2 = i.findAll("a", {"target":"_blank"})
             for a in a_h2:
                 if 'href' in a.attrs:  # 내부에 있는 항목들을 리스트로 가져옵니다 ex) {u'href': u'//www.wikimediafoundation.org/'}
                     # print(a.attrs['href'])
                     b = a.attrs['href']
                     url_list.append(b)
        page = page + 10
    # for i in url_list:
    #     print(i)

    j_crawl(url_list)


def j_crawl(lista):
    ps_name = "중앙일보"
    text_list = []
    for i in lista:
    #     print(i)
        url = i
        response = requests.get(url)
        html = response.text
        objBS = bs4.BeautifulSoup(html, "html.parser")
        news_infos = objBS.findAll("div", {"id": "article_body"})

        for x in news_infos:
            v = x.text.strip().replace("\n", "")
            # b = v.replace("// flash 오류를 우회하기 위한 함수 추가", "").replace("function _flash_removeCallback() {}", "")
            text_list.append(v.strip())
            text_list = list(set(text_list))
    # for i, j in enumerate(text_list):
    #     print(i+1, j)
    save(ps_name, text_list)
    # print("==========================================")




def k_url(url_info, sort, maxpage):

    pn = 1
    url_list = []

    while (pn <= int(maxpage)):
        url = "https://search.hankyung.com/apps.frm/search.news?query=" + url_info + "&sort="+ sort +"%2FDESC%2CDATE%2FDESC&period=ALL&area=ALL&mediaid_clust=HKPAPER%2CHKCOM&exact=&include=&except=&page=" + str(
            pn)

        # print("{} 페이지".format(pn))
        pn = pn + 1
        response = requests.get(url)
        html = response.text
        objBS = bs4.BeautifulSoup(html, "html.parser")

        news_infos = objBS.findAll("ul", {"class": "article"})
        # print(news_infos)
        for i in news_infos:
            a_li = i.findAll("a", {"target": "_blank"})
            for a in a_li:
                if 'href' in a.attrs:
                    b = a.attrs['href']
                    url_list.append(b)
                    url_list = list(set(url_list))

        # for i in url_list:
        #     print(i)
    k_crawl(url_list)


def k_crawl(lists):
    ps_name = "한국경제"
    page_list = []
    text_list = []
    for i in lists:
        url = i
        response = requests.get(url)
        html = response.text
        objBS = bs4.BeautifulSoup(html, "html.parser")
        news_infos = objBS.findAll("div", {"id": "articletxt"})
        for x in news_infos:
            v = x.text.strip().replace("\n", "")
            text_list.append(v)
            text_list = list(set(text_list))
        # c_list = [x for x in text_list if x]
    # for i, j in enumerate(c_list):
    #     print(i+1, j)
    save(ps_name, text_list)
    # print("==========================================")
    # save(text_list)




def h_url(url_info, sort, maxpage):
    maxpage = int(maxpage)
    url_list = []

    # print("\n")
    page = 0
    while (page <= (maxpage-1)):
        url = "http://search.hani.co.kr/Search?command=query&keyword=" + url_info + "&media=news&submedia=&sort="+sort+"&period=all&datefrom=2000.01.01&dateto=2019.07.26&pageseq=" + str(
            page)
        # print(url)
        response = requests.get(url)
        html = response.text
        objBS = bs4.BeautifulSoup(html, "html.parser")
        news_infos = objBS.findAll("ul", {"class": "search-result-list"})


        for i in news_infos:
            a_li = i.findAll("a")
            # print(a_li)
            for a in a_li:
                if 'href' in a.attrs:
                    c = a.attrs['href']
                    url_list.append(c)
                    url_list = list(set(url_list))
        # for i in url_list:
        #     print(i)
        page = page + 1
        # print("\n")
    h_crawl(url_list)



def h_crawl(list):
    ps_name = "한겨례"
    text_list = []
    for i in list:
        url = i
        response = requests.get(url)
        html = response.text
        objBS = bs4.BeautifulSoup(html, "html.parser")
        news_infos = objBS.findAll("div", {"class": "text"})
        for x in news_infos:
            z = x.text.strip().replace("\n", "")
            # print(z)
            text_list.append(z.strip())
    # for i, j in enumerate(text_list):
    #     print(i+1, j.strip())
    save(ps_name, text_list)
    # print("==========================================")


def blog_url(url_info, sort, maxpage):
    page = 1
    pn = 1
    maxpage_t = (int(maxpage) - 1) * 10 + 1
    url_list = []

    while(page <= maxpage_t):
        url = "https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove="+sort+"&nso=&post_blogurl=&post_blogurl_without=&query="+url_info+"&sm=tab_pge&srchby=all&st=sim&where=post&start=" + str(page)
        # print("{} 페이지".format(pn))
        pn = pn + 1
        response = requests.get(url)
        html = response.text
        objBS = bs4.BeautifulSoup(html, "html.parser")
        news_infos = objBS.findAll("ul", {"class": "type01"})
        # print(news_infos)
        for i in news_infos:
            a_li = i.findAll("a", {"class": "_sp_each_url"})
            for a in a_li:
                if 'href' in a.attrs:
                    b = a.attrs['href']
                    url_list.append(b)
        page = page + 10
    for i in url_list:
        print(i)
        # print("==========================")

    Bcrawl(url_list)


def Bcrawl(listt):
    ps_name = "네이버 블로그"
    url1 = []
    text_list = []
    blogurl = "https://blog.naver.com/"
    for i in listt:
        url = i
        response = requests.get(url)
        html = response.text.encode('utf-8')
        objBS = bs4.BeautifulSoup(html, "html.parser")
        # print(objBS)
        see = objBS.findAll('iframe',{'id':'mainFrame'})
        url1.append(see)
        url2 = []
        for i in see:
            if 'src' in i.attrs:
                v = i.attrs['src']
                c = blogurl + v
                url2.append(c)
        for i in url2:
            response = requests.get(i)
            html = response.text
            objBSsa = bs4.BeautifulSoup(html, "html.parser")
            # print(objBSsa)
            temp = objBSsa.findAll("div", {"class": "se-main-container"})
            for a in temp:
                text = a.get_text().replace("\n", "")
                # print(text.strip())
                text_list.append(text)
                text_list = list(set(text_list))
    # for i, j in enumerate(text_list):
    #     print(i+1, j)
    save(ps_name, text_list)



def save(ps_name, list):
    RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/BD/craw/'  # 결과 저장할 경로/파일명
    now = datetime.now()  # 파일이름 현 시간으로 저장하기

    # 모든 리스트 딕셔너리형태로 저장
    result = {"source": ps_name, "contents": list}

    df = pd.DataFrame(result)  # df로 변환

    outputFileName = ps_name + '%s-%s-%s  %s시 %s분 %s초.csv' % (
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_csv(RESULT_PATH + outputFileName, mode='w')
    # merge()


def read_csv(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    print(df)

def merge():

    RESULT_PATH = 'C:/Users/wnstj/PycharmProjects/untitled/crawling/result/크롤링'  # 결과 저장할 경로/파일명
    now = datetime.now()  # 파일이름 현 시간으로 저장하기
    outputFileName = '%s-%s-%s  %s시 %s분 %s초.csv' % (
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    c = glob.glob('*.csv')


    for i in c:
        df = pd.read_csv(i, encoding='utf-8')
        df2 = df[["source", "contents"]]
        df2.to_csv(RESULT_PATH + '합치기' + outputFileName, mode='a')

    read_csv(RESULT_PATH + '합치기' + outputFileName)

def read_csv(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    print(df)

inputinfo()
